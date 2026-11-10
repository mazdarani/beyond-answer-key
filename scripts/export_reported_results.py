#!/usr/bin/env python3
"""Export published table values. This does not reconstruct benchmark samples."""

import argparse
import csv
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = (
    ("I", "GPT-OSS 20B", "table_i_gpt_oss_20b.tex"),
    ("II", "Qwen3-14B", "table_ii_qwen3_14b.tex"),
    ("III", "Phi-4-Reasoning", "table_iii_phi_4_reasoning.tex"),
)
VARIANTS = ("Base", "Base + TTC", "FT", "FT + TTC", "GED-FT", "GED-FT + TTC")
QUERIES = ("Q1", "Q2", "Q3")
GROUPS = ("overall", "T1", "T2", "T3")
VALUE_COLUMNS = [f"{q}_{group}_pct" for q in QUERIES for group in GROUPS]


def read_source_rows():
    rows = []
    for table, model, filename in TABLES:
        text = (ROOT / "source" / "tables" / filename).read_text()
        sections = re.split(
            r"\\multicolumn\{13\}\{l\}\{\\textbf\{(?:Baseline|Perturbed)\}\}", text
        )
        if len(sections) != 3:
            raise ValueError(f"Expected canonical and perturbed sections in {filename}")
        for split, section in zip(("canonical", "perturbed"), sections[1:]):
            matches = list(re.finditer(
                r"^(Base(?: \+ TTC)?|FT(?: \+ TTC)?|GED-FT(?: \+ TTC)?)\s*\n"
                r"(.*?)(?=^Base|^FT|^GED-FT|\\bottomrule|\\midrule|\Z)",
                section, re.M | re.S,
            ))
            if [m[1] for m in matches] != list(VARIANTS):
                raise ValueError(f"Unexpected variants in {filename}, {split}")
            for match in matches:
                values = re.findall(r"\\hm\{(\d+(?:\.\d+)?)\}", match[2])
                if len(values) != 12:
                    raise ValueError(f"Expected 12 values: {filename}, {split}, {match[1]}")
                rows.append({
                    "table": table, "model": model, "split": split,
                    "variant": match[1], **dict(zip(VALUE_COLUMNS, values)),
                })
    return rows


def csv_text(rows, fieldnames):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def expected_exports():
    rows = read_source_rows()
    long_rows = []
    for row in rows:
        for query in QUERIES:
            for group in GROUPS:
                long_rows.append({
                    **{k: row[k] for k in ("table", "model", "split", "variant")},
                    "query": query, "trace_group": group,
                    "accuracy_pct": row[f"{query}_{group}_pct"],
                    "paper_reported_n": 1080 if group == "overall" else 360,
                    "provenance": "published_aggregate_table",
                })
    return {
        "results_wide.csv": csv_text(rows, ["table", "model", "split", "variant"] + VALUE_COLUMNS),
        "results_long.csv": csv_text(long_rows, list(long_rows[0])),
        # Strings preserve the original published precision, including trailing zeros.
        "results_wide.json": json.dumps(rows, indent=2) + "\n",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check exports without writing files")
    args = parser.parse_args()
    for name, expected in expected_exports().items():
        path = ROOT / "data" / "reported_results" / name
        if args.check:
            if not path.is_file() or path.read_text() != expected:
                raise SystemExit(f"Export differs from source tables: {path.relative_to(ROOT)}")
        else:
            path.write_text(expected)
    print("Verified 36 result rows and 432 published accuracy values." if args.check
          else "Exported 36 result rows and 432 published accuracy values.")


if __name__ == "__main__":
    main()
