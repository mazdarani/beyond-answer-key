#!/usr/bin/env python3
"""Verify the integrity and scope of the recovered materials."""

import csv
import hashlib
import itertools
import json
from decimal import Decimal
from pathlib import Path

from export_reported_results import ROOT, TABLES, VALUE_COLUMNS, VARIANTS, expected_exports


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    expected_files = set()
    for line in (ROOT / "metadata/checksums.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        relative = Path(name)
        require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe manifest path")
        path = ROOT / relative
        require(path.is_file(), f"Missing file: {name}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest, f"Checksum mismatch: {name}")
        require(name not in expected_files, f"Duplicate manifest path: {name}")
        expected_files.add(name)

    for filename, expected in expected_exports().items():
        path = ROOT / "data/reported_results" / filename
        require(path.read_text() == expected, f"Export differs from source: {filename}")
    with (ROOT / "data/reported_results/results_wide.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    expected_keys = set(itertools.product(
        (model for _, model, _ in TABLES), ("canonical", "perturbed"), VARIANTS
    ))
    actual_keys = [(r["model"], r["split"], r["variant"]) for r in rows]
    require(len(rows) == 36 and set(actual_keys) == expected_keys, "Unexpected result coverage")
    for row in rows:
        for column in VALUE_COLUMNS:
            require(Decimal(0) <= Decimal(row[column]) <= Decimal(100), "Out-of-range accuracy")

    inventory = json.loads((ROOT / "metadata/release_inventory.json").read_text())
    require(inventory["original_benchmark_available"] is False, "Update the release verifier for a complete release")
    require(inventory["release_status"] == "partial_recovery", "Release scope differs from this package")
    settings = json.loads((ROOT / "configs/paper_reported_settings.json").read_text())
    require(settings["status"] == "descriptive_transcription_not_executable_configuration", "Settings scope changed")
    crosscheck = json.loads((ROOT / "metadata/pdf_crosscheck.json").read_text())
    provenance = json.loads((ROOT / "metadata/provenance.json").read_text())
    require(crosscheck["accuracy_values_compared"] == 432 and crosscheck["mismatches"] == 0, "Incomplete PDF cross-check")
    require(crosscheck["published_pdf_sha256"] == provenance["paper"]["published_pdf_sha256"], "PDF identity differs")

    source_members = {
        member["filename"]: member["sha256"]
        for archive in provenance["recovered_archives"]
        if archive["filename"] == "beyond_answer_key_camera_ready.zip"
        for member in archive["members"]
    }
    figures = sorted((ROOT / "figures").glob("*.png"))
    require(len(figures) == 3, "Expected three recovered figures")
    for path in figures:
        require(path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), f"Invalid PNG: {path.name}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == source_members[path.name], f"Figure differs from original: {path.name}")

    # Ignore local Git internals and Python cache files when checking manifest coverage.
    actual_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(p in {".git", "__pycache__"} for p in path.relative_to(ROOT).parts)
        and path.name != ".DS_Store"
    }
    require(actual_files == expected_files | {"metadata/checksums.sha256"}, "Manifest file coverage differs")
    print(f"Verified {len(expected_files)} file hashes, 432 published values, three original figures, and partial-release metadata.")
    print("Original trace-level benchmark: not included.")


if __name__ == "__main__":
    main()
