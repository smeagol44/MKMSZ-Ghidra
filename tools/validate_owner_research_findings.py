#!/usr/bin/env python3
"""Crosscheck scoped research findings against canonical owner claim IDs.

To revalidate against a current separate Wiki checkout:
  python tools/validate_owner_research_findings.py --wiki-dir ../MKMSZ-Randomizer/wiki
A source hash mismatch means review is required; do not infer contradiction or
rewrite another investigator's current findings automatically.
"""
import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/"analysis"/name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir",type=Path,default=None)
    args=parser.parse_args()
    facts=read("owner_research_findings.tsv")
    claims={r["fact_id"]:r for r in read("known_knowledge_claims.tsv")}
    owners={r["owner_page"]:r for r in read("known_knowledge_owners.tsv")}
    assert len(facts)==len({r["fact_id"] for r in facts})==40
    source_pages={x["owner_page"] for x in facts}
    assert len(source_pages)==5
    assert {sum(r["owner_page"]==page for r in facts) for page in source_pages}=={8}
    for r in facts:
        id=r["fact_id"]
        assert r["owner_page"] in owners and owners[r["owner_page"]]["reconciliation"]=="partial-crosswalk"
        assert r["source_blob_sha"] and len(r["source_blob_sha"])==40
        assert all(r[k] for k in ("source_anchor","documented_excerpt","scope","source_section","limitations"))
        c=claims[id]
        assert c["target_path"]=="analysis/owner_research_findings.tsv" and c["target_key"]==id
        assert c["wiki_source_anchor"]==r["source_anchor"] and c["owner_page"]==r["owner_page"]
    if args.wiki_dir:
        for page in source_pages:
            p=args.wiki_dir/page
            raw=p.read_bytes()
            git_sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
            expected={r["source_blob_sha"] for r in facts if r["owner_page"]==page}
            assert expected=={git_sha},f"Wiki source revision changed: {page}; review current owner before reuse"
            decoded=raw.decode("utf-8")
            for f in facts:
                if f["owner_page"]==page:
                    assert f["source_anchor"].lower() in decoded.lower(),f"Stale source anchor: {f['fact_id']}"
    print("40 scoped facts across five existing owners validated; no new Ghidra functions.")

if __name__ == "__main__":
    main()
