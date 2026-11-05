#!/usr/bin/env python3
"""Embed a CFTR2 variant list (xlsx from cftr2.org, "Variant List History") into index.html.

Usage: python3 tools/build_cftr2.py data/CFTR2_<date>.xlsx [index.html]

Replaces the contents of <script id="cftr2-data" type="application/json"> in the page.
Row format: [legacy, protein, cDNA, altNames, alleles, freq, det, prevDet, isNew, g38[], g37[]]
det codes: C = CF-causing, V = Varying clinical consequence, N = Non CF-causing, U = no interpretation.
g38/g37 entries are "pos:ref:alt" on chromosome 7.
"""
import json
import re
import sys

import openpyxl

CODES = {
    "cf-causing": "C",
    "varying clinical consequence": "V",
    "non cf-causing": "N",
    "no interpretation available": "U",
}


def code(v):
    if not v:
        return ""
    k = str(v).strip().lower()
    if k not in CODES:
        raise SystemExit(f"Unknown determination: {v!r}")
    return CODES[k]


def num(v, cast):
    """Numeric cell, or None when CFTR2 gives text (e.g. 'see note below')."""
    try:
        return cast(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def main():
    src = sys.argv[1]
    page = sys.argv[2] if len(sys.argv) > 2 else "index.html"
    wb = openpyxl.load_workbook(src, read_only=True)
    ws, wg = wb.worksheets[0], wb.worksheets[1]
    rows = list(ws.iter_rows(values_only=True))

    meta = {}
    for r in rows[:12]:
        t = str(r[0] or "")
        m = re.match(r"Date:\s*(.+)", t)
        if m:
            meta["date"] = m.group(1).strip()
        m = re.match(r"Number of patients in CFTR2:\s*([\d,]+)", t)
        if m:
            meta["patients"] = int(m.group(1).replace(",", ""))
        m = re.match(r"CFTR reference transcript:\s*(\S+)", t)
        if m:
            meta["transcript"] = m.group(1)

    hdr = next(i for i, r in enumerate(rows) if r[0] == "Variant legacy name")
    h = rows[hdr]
    m = re.search(r"of (\d+) identified alleles", str(h[5]))
    meta["alleles"] = int(m.group(1)) if m else None
    m = re.search(r"determination (.+?) \(previous", str(h[6]))
    meta["prevDate"] = m.group(1) if m else ""

    # genomic coordinates keyed by (legacy, cDNA)
    coords = {}
    for r in list(wg.iter_rows(values_only=True))[1:]:
        if not r[1]:
            continue
        key = str(r[1]).strip()
        e = coords.setdefault(key, {"g38": [], "g37": []})
        if r[6] and r[7] and r[8]:
            e["g37"].append(f"{r[6]}:{r[7]}:{r[8]}")
        if r[10] and r[11] and r[12]:
            e["g38"].append(f"{r[10]}:{r[11]}:{r[12]}")

    out = []
    for r in rows[hdr + 1:]:
        if not r[0] or not r[2]:
            continue
        legacy = str(r[0]).strip()
        c = coords.get(legacy, {"g38": [], "g37": []})
        out.append([
            legacy,
            str(r[1] or "").strip(),
            str(r[2]).strip(),
            str(r[3] or "").strip(),
            num(r[4], int),
            num(r[5], lambda x: round(float(x), 7)),
            code(r[7]),
            code(r[6]),
            1 if str(r[8] or "").lower().startswith("yes") else 0,
            c["g38"],
            c["g37"],
        ])
    meta["n"] = len(out)

    blob = json.dumps({"meta": meta, "v": out}, separators=(",", ":"), ensure_ascii=False)
    blob = blob.replace("</", "<\\/")
    html = open(page, encoding="utf-8").read()
    pat = re.compile(r'(<script id="cftr2-data" type="application/json">)(.*?)(</script>)', re.S)
    if not pat.search(html):
        raise SystemExit("data block not found in page")
    html = pat.sub(lambda m: m.group(1) + blob + m.group(3), html, count=1)
    open(page, "w", encoding="utf-8").write(html)
    print(f"{meta['n']} variants, CFTR2 {meta.get('date')}, {len(blob)/1024:.0f} KB embedded")


if __name__ == "__main__":
    main()
