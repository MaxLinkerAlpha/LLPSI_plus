#!/usr/bin/env python3
"""
query_isbn.py — 通过 Open Library / Google Books API 查询 ISBN 元信息
                (无网络时跳过, 仅依赖 OCR 提取)
"""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 优先使用 v2 (改进语言判定), 兼容 v1
META_FILE = ROOT / "analysis_output" / "reader_metadata_v2.json"
if not META_FILE.exists():
    META_FILE = ROOT / "analysis_output" / "reader_metadata.json"
ENRICHED = ROOT / "analysis_output" / "reader_metadata_enriched.json"

# Open Library 单本查询 URL
OL_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"


def query_openlibrary(isbn: str) -> dict | None:
    url = OL_URL.format(isbn=isbn)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LLPSI/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            key = f"ISBN:{isbn}"
            if key in data:
                book = data[key]
                return {
                    "title": book.get("title"),
                    "authors": [a.get("name") for a in book.get("authors", [])],
                    "publish_date": book.get("publish_date"),
                    "publishers": [p.get("name") for p in book.get("publishers", [])],
                    "subjects": [s.get("name") for s in book.get("subjects", [])][:10],
                    "page_count": book.get("number_of_pages"),
                    "cover": (book.get("cover") or {}).get("small"),
                    "url": book.get("url"),
                }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  [WARN] OL {isbn}: {e}", file=sys.stderr)
    return None


def main() -> int:
    if not META_FILE.exists():
        print(f"[错误] 找不到 {META_FILE}, 请先运行 extract_metadata.py")
        return 1
    data = json.loads(META_FILE.read_text(encoding="utf-8"))

    enriched = []
    n_query = 0
    for entry in data:
        if entry.get("status") != "ok":
            enriched.append(entry)
            continue
        isbn = entry.get("isbn")
        entry_out = dict(entry)
        if isbn and len(isbn) in (10, 13):
            print(f"[查询] {entry['slug']:<35} ISBN={isbn}")
            ol = query_openlibrary(isbn)
            if ol:
                entry_out["openlibrary"] = ol
                n_query += 1
            else:
                entry_out["openlibrary"] = None
            time.sleep(0.5)  # 礼貌速率限制
        else:
            entry_out["openlibrary"] = None
        enriched.append(entry_out)

    ENRICHED.write_text(json.dumps(enriched, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"\n[完成] {n_query} 个 ISBN 已查询, 写入 {ENRICHED}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
