#!/usr/bin/env python3
"""
ocr_new_ecce_romani.py — 完整 OCR 3 本新 Ecce Romani PDF
(IIA, IIB, III) + 解析 I&II Combined EPUB

输出:
  - ocr_output/ecce_romani_2a/{page_NNN.txt, _full.txt}
  - ocr_output/ecce_romani_2b/{page_NNN.txt, _full.txt}
  - ocr_output/ecce_romani_3/{page_NNN.txt, _full.txt}
  - ocr_output/ecce_romani_combined/{_full.txt}  (EPUB 解析)
  - analysis_output/batch_ocr_status_v2.json
"""
import json
import os
import subprocess
import sys
import time
import traceback
import zipfile
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "Other_Readers" / "拉英-快看罗马人EcceRomani"
OCR_OUT = ROOT / "ocr_output"
STATUS_FILE = ROOT / "analysis_output" / "batch_ocr_status_v2.json"

DPI = 250
WORKERS = 3  # 3 PDFs in parallel
RETRY = 1

# 3 PDFs to OCR
PDF_TASKS = [
    ("ecce_romani_2a", SRC / "Ecce Romani IIA - STUDENT EDITION (SOFTCOVER) 2005 C (PRENTICE HALL) .pdf"),
    ("ecce_romani_2b", SRC / "Ecce Romani IIB (Student ManualStudy Guide) (Addison Wesley) .pdf"),
    ("ecce_romani_3", SRC / "Ecce Romani III. (Perry, David J.) .pdf"),
]

# EPUB
EPUB_PATH = SRC / "Ecce Romani I&II Combined A Latin Reading Program (Scottish Classics Group).epub"
EPUB_SLUG = "ecce_romani_combined"


def ocr_pdf(slug: str, pdf_path: Path, dpi: int = DPI) -> dict:
    """OCR 一本 PDF. 调用 ocr_book.py."""
    cmd = [
        "python3", str(ROOT / "scripts" / "ocr_book.py"),
        "--pdf", str(pdf_path),
        "--slug", slug,
        "--output-root", str(OCR_OUT),
        "--dpi", str(dpi),
        "--workers", "2",
    ]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
        elapsed = time.time() - t0
        if r.returncode == 0:
            pages = 0
            for line in r.stdout.splitlines():
                if "共处理" in line and "页" in line:
                    try:
                        pages = int(line.split("共处理")[1].split("页")[0].strip())
                    except Exception:
                        pass
            return {"slug": slug, "kind": "pdf_ocr", "pages": pages,
                    "elapsed_s": elapsed, "status": "ok", "error": None}
        else:
            # 重试 1 次
            if RETRY > 0:
                print(f"[{slug}] 失败, 重试...")
                r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
                if r2.returncode == 0:
                    pages = 0
                    for line in r2.stdout.splitlines():
                        if "共处理" in line and "页" in line:
                            try:
                                pages = int(line.split("共处理")[1].split("页")[0].strip())
                            except Exception:
                                pass
                    return {"slug": slug, "kind": "pdf_ocr", "pages": pages,
                            "elapsed_s": time.time() - t0, "status": "ok_retry", "error": None}
            return {"slug": slug, "kind": "pdf_ocr", "pages": 0,
                    "elapsed_s": elapsed, "status": "failed",
                    "error": r.stderr[-500:] if r.stderr else "unknown"}
    except subprocess.TimeoutExpired:
        return {"slug": slug, "kind": "pdf_ocr", "pages": 0,
                "elapsed_s": time.time() - t0, "status": "timeout",
                "error": "subprocess timeout"}
    except Exception as e:
        return {"slug": slug, "kind": "pdf_ocr", "pages": 0,
                "elapsed_s": time.time() - t0, "status": "exception",
                "error": str(e)}


def extract_epub(slug: str, epub_path: Path) -> dict:
    """解析 EPUB, 提取所有 xhtml 内容, 保存为 _full.txt."""
    t0 = time.time()
    try:
        out_dir = OCR_OUT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        full_txt = out_dir / "_full.txt"

        text_files_data = []
        with zipfile.ZipFile(epub_path, 'r') as z:
            for name in z.namelist():
                if not (name.endswith('.xhtml') or name.endswith('.html')) or name.endswith('toc.ncx'):
                    continue
                info = z.getinfo(name)
                if info.file_size < 500:  # skip empty leaf placeholders
                    continue
                with z.open(name) as f:
                    html = f.read().decode('utf-8', errors='replace')
                # Strip HTML tags
                html_clean = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
                html_clean = re.sub(r'</(p|div|h[1-6]|li|tr)>', '\n', html_clean, flags=re.IGNORECASE)
                html_clean = re.sub(r'<br[^>]*>', '\n', html_clean, flags=re.IGNORECASE)
                text = re.sub(r'<[^>]+>', ' ', html_clean)
                text = unescape(text)
                text = re.sub(r'[ \t]+', ' ', text)
                text = re.sub(r'\n\s*\n+', '\n\n', text).strip()
                if len(text) > 100:
                    text_files_data.append((name, text))

        # Save individual page-like files (chapters) and full text
        for i, (name, text) in enumerate(text_files_data, 1):
            (out_dir / f"page_{i:03d}.txt").write_text(text, encoding='utf-8')

        full_content = "\n\n".join(f"=== {name} ===\n\n{text}" for name, text in text_files_data)
        full_txt.write_text(full_content, encoding='utf-8')

        return {"slug": slug, "kind": "epub_extract", "pages": len(text_files_data),
                "elapsed_s": time.time() - t0, "status": "ok", "error": None,
                "char_count": len(full_content)}
    except Exception as e:
        return {"slug": slug, "kind": "epub_extract", "pages": 0,
                "elapsed_s": time.time() - t0, "status": "exception",
                "error": f"{e}\n{traceback.format_exc()[:300]}"}


def main() -> int:
    print(f"=== OCR 3 本新 Ecce Romani PDF + 解析 I&II Combined EPUB ===")
    print(f"DPI: {DPI}, Workers: {WORKERS}")
    print(f"OCR 输出: {OCR_OUT}")
    print(f"状态记录: {STATUS_FILE}")
    print()

    all_results = []

    # 第一步: 3 本 PDF 并行 OCR
    print("--- Step 1: OCR 3 本 PDF (3 workers parallel) ---")
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        future_to_task = {
            executor.submit(ocr_pdf, slug, path): (slug, path)
            for slug, path in PDF_TASKS
        }
        for fut in as_completed(future_to_task):
            slug, path = future_to_task[fut]
            try:
                r = fut.result()
                all_results.append(r)
                print(f"  [{slug}] {r['status']} | {r['pages']} pages | {r['elapsed_s']:.0f}s")
            except Exception as e:
                print(f"  [{slug}] exception: {e}")
                all_results.append({"slug": slug, "kind": "pdf_ocr", "status": "exception", "error": str(e)})

    # 第二步: 解析 EPUB
    print()
    print("--- Step 2: 解析 Ecce Romani I&II Combined EPUB ---")
    r = extract_epub(EPUB_SLUG, EPUB_PATH)
    all_results.append(r)
    print(f"  [{EPUB_SLUG}] {r['status']} | {r['pages']} pages | {r['elapsed_s']:.1f}s | {r.get('char_count', 0):,} chars")

    # 保存状态
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump({"started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "results": all_results}, f, ensure_ascii=False, indent=2)

    print()
    print(f"=== 完成 ===")
    for r in all_results:
        flag = "OK" if r["status"].startswith("ok") else "FAIL"
        print(f"  [{flag}] {r['slug']:30s} {r['kind']:15s} {r['pages']} pages")

    return 0 if all(r["status"].startswith("ok") for r in all_results) else 1


if __name__ == "__main__":
    sys.exit(main())
