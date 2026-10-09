#!/usr/bin/env python3
"""Verify nine-page first-pass knowledge index and complete heading navigation.

This confirms source-provenance pointers and catalog coverage, NOT that those
nine extensive Wiki owners are exhaustively migrated into Ghidra.
"""
import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/"analysis"/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--wiki-dir",type=Path,default=None)
    args=p.parse_args()
    findings=read("remaining_owner_facts.tsv")
    sections=read("remaining_owner_sections.tsv")
    claims={c["fact_id"]:c for c in read("known_knowledge_claims.tsv")}
    owners={o["owner_page"]:o for o in read("known_knowledge_owners.tsv")}
    assert len(findings)==54 and len(sections)==242
    assert len({f["fact_id"] for f in findings})==54
    assert len({s["section_id"] for s in sections})==242
    counts=Counter(f["owner_page"] for f in findings)
    assert len(counts)==9 and set(counts.values())=={6}
    assert set(s["owner_page"] for s in sections)==set(counts)
    by_page={}
    for row in findings:
        key=row["fact_id"]
        assert owners[row["owner_page"]]["reconciliation"]=="partial-crosswalk"
        assert claims[key]["target_path"]=="analysis/remaining_owner_facts.tsv"
        assert claims[key]["target_key"]==key and claims[key]["wiki_source_anchor"]==row["source_anchor"]
        assert claims[key]["owner_page"]==row["owner_page"]
        assert row["source_anchor"] and row["source_line"].isdigit() and row["documented_excerpt"]
        assert len(row["source_blob_sha"])==40 and row["evidence_boundary"]
        by_page.setdefault(row["owner_page"],set()).add(row["source_blob_sha"])
    lines_by_page={}
    for row in sections:
        assert row["review_status"]=="indexed-heading-not-fully-audited"
        assert row["depth"] in ("2","3")
        assert 0<int(row["section_line"])<int(row["end_line_exclusive"])
        assert row["heading"].strip() and len(row["source_blob_sha"])==40
        assert row["source_blob_sha"] in by_page[row["owner_page"]]
        lines_by_page.setdefault(row["owner_page"],[]).append(int(row["section_line"]))
    assert all(vals==sorted(vals) for vals in lines_by_page.values())
    if args.wiki_dir:
        for page in counts:
            raw=(args.wiki_dir/page).read_bytes()
            actual=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
            assert by_page[page]=={actual},f"Wiki changed, review provenance: {page}"
            ls=raw.decode("utf-8").split("\n")
            for row in sections:
                if row["owner_page"]==page:
                    actual_heading=ls[int(row["section_line"])-1].lstrip("# ").replace("|","¦")
                    assert actual_heading==row["heading"],row["section_id"]
            for row in findings:
                if row["owner_page"]==page:
                    line=ls[int(row["source_line"])-1]
                    assert row["source_anchor"].lower() in line.lower(),row["fact_id"]
    print("Nine owner first-passes: 54 verified provenance claims and 242 section index entries.")
    print("All nine remain PARTIAL; section navigation is not full semantic migration.")
if __name__=="__main__":
    main()
