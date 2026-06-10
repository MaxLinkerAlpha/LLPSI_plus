#!/usr/bin/env python3
"""
batch_ocr_readers.py — 多进程并行 OCR 全部非 C 类读物 (52 本)

策略:
  - 4 个 worker 进程同时 OCR 4 本书
  - DPI 250 平衡速度与质量
  - 失败重试 1 次
  - 状态记录到 analysis_output/batch_ocr_status.json
  - 输出到 ocr_output/<slug>/page_NNN.txt + _full.txt
"""

import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from queue import Queue
from threading import Thread

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "Other_Readers" / "curated"
OCR_OUT = ROOT / "ocr_output"
STATUS_FILE = ROOT / "analysis_output" / "batch_ocr_status.json"

# DPI 选择: 250 是 拉语 OCR 较优平衡点 (150-200 偏粗, 350+ 慢且过采)
DPI = 250
WORKERS = 4
RETRY = 1


def scan_books() -> list:
    """扫描 curated/ 下所有 symlink, 返回 [(slug, abs_path), ...]"""
    books = []
    for tier_dir in sorted(SRC.iterdir()):
        if not tier_dir.is_dir():
            continue
        tier = tier_dir.name
        for link in sorted(tier_dir.iterdir()):
            if not link.is_symlink():
                continue
            target = link.resolve()
            if not target.exists():
                continue
            slug = link.stem
            books.append((slug, str(target), tier))
    return books


def ocr_one_book(slug: str, pdf_path: str, dpi: int = DPI) -> dict:
    """
    调用 ocr_book.py 处理单本书.
    返回 {"slug", "pages", "elapsed_s", "status", "error"}
    """
    import subprocess
    cmd = [
        "python3", str(ROOT / "scripts" / "ocr_book.py"),
        "--pdf", pdf_path,
        "--slug", slug,
        "--output-root", str(OCR_OUT),
        "--dpi", str(dpi),
        "--workers", "2",  # 每本内部用 2 线程, 4 本 × 2 = 8 核利用率
    ]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        elapsed = time.time() - t0
        if r.returncode == 0:
            # 解析处理页数
            pages = 0
            for line in r.stdout.splitlines():
                if "共处理" in line and "页" in line:
                    try:
                        pages = int(line.split("共处理")[1].split("页")[0].strip())
                    except Exception:
                        pass
            return {"slug": slug, "pages": pages, "elapsed_s": elapsed,
                    "status": "ok", "error": None}
        else:
            return {"slug": slug, "pages": 0, "elapsed_s": elapsed,
                    "status": "error", "error": r.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"slug": slug, "pages": 0, "elapsed_s": 3600,
                "status": "timeout", "error": "OCR 超过 3600s"}
    except Exception as e:
        return {"slug": slug, "pages": 0, "elapsed_s": time.time() - t0,
                "status": "exception", "error": str(e)[:500]}


def process_with_retry(slug: str, pdf_path: str) -> dict:
    """失败重试 1 次"""
    result = ocr_one_book(slug, pdf_path)
    if result["status"] != "ok" and RETRY > 0:
        print(f"  [重试] {slug}", flush=True)
        time.sleep(2)
        result = ocr_one_book(slug, pdf_path)
        result["retried"] = True
    return result


def main() -> int:
    books = scan_books()
    print(f"[信息] 待处理: {len(books)} 本非 C 类书籍")
    print(f"[信息] DPI={DPI}, 并行={WORKERS}, 重试={RETRY}")

    # 跳过已完成的 (按 _full.txt 是否存在)
    pending = []
    for slug, pdf, tier in books:
        full = OCR_OUT / slug / "_full.txt"
        if full.exists() and full.stat().st_size > 100:
            print(f"  [SKIP] {slug} (已有 {full.stat().st_size} 字节)")
            continue
        pending.append((slug, pdf, tier))

    print(f"[信息] 待执行: {len(pending)} 本")
    if not pending:
        return 0

    # 进度回报
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    results = []
    t_start = time.time()

    # 使用进程池 (multiprocessing) 跨书并行
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        future_to_book = {
            executor.submit(process_with_retry, slug, pdf): (slug, tier)
            for slug, pdf, tier in pending
        }
        for fut in as_completed(future_to_book):
            slug, tier = future_to_book[fut]
            try:
                result = fut.result()
            except Exception as e:
                result = {"slug": slug, "pages": 0, "elapsed_s": 0,
                          "status": "exception", "error": str(e)}
            result["tier"] = tier
            results.append(result)
            # 进度
            done = len(results)
            total = len(pending)
            elapsed = time.time() - t_start
            rate = done / elapsed if elapsed > 0 else 0
            eta = (total - done) / rate if rate > 0 else 0
            pages = result.get("pages", 0)
            status_icon = {"ok": "✓", "error": "✗", "timeout": "T", "exception": "E"}.get(
                result["status"], "?")
            print(f"  [{done:>3}/{total}] {status_icon} {slug:<35} "
                  f"页={pages:>4} 用时={result.get('elapsed_s', 0):.0f}s "
                  f"ETA={eta:.0f}s", flush=True)

    # 写状态
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "started_at": t_start,
            "finished_at": time.time(),
            "dpi": DPI,
            "workers": WORKERS,
            "total_books": len(books),
            "pending_count": len(pending),
            "results": results,
        }, f, ensure_ascii=False, indent=2)

    # 汇总
    ok = sum(1 for r in results if r["status"] == "ok")
    fail = len(results) - ok
    total_pages = sum(r.get("pages", 0) for r in results if r["status"] == "ok")
    total_time = time.time() - t_start
    print(f"\n[汇总] 成功 {ok}/{len(results)}, 失败 {fail}, "
          f"总页数 {total_pages}, 总耗时 {total_time:.0f}s")
    if fail:
        print("[失败清单]")
        for r in results:
            if r["status"] != "ok":
                print(f"   {r['slug']:<35} {r['status']}: {r.get('error', '')[:100]}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
