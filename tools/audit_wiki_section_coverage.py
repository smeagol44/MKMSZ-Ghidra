#!/usr/bin/env python3
"""Audit documented Wiki sections against already-known fact anchors.

This is a source-navigation coverage report, NOT an automatic certificate that
every fact in a section was migrated. No network, ROM, emulator or Ghidra needed.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def tsv(filename):
    with (ROOT/"analysis"/filename).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))

def sections(page,text,sha):
    lines=text.split("\n")
    headers=[]
    for i,line in enumerate(lines):
        if line.startswith("## ") or line.startswith("### "):
            headers.append((i+1,len(line)-len(line.lstrip("#")),line.lstrip("# ").strip()))
    records=[]
    for n,(start,depth,title) in enumerate(headers):
        end=headers[n+1][0] if n+1<len(headers) else len(lines)+1
        records.append({"owner_page":page,"start_line":start,
                        "end_line_exclusive":end,"depth":depth,"heading":title,
                        "source_blob_sha":sha,"unique_claims":0})
    return records

def analyze(owners,claims,raw_files):
    records=[]
    missing=[]
    ambiguous=[]
    preamble=[]
    registered={o["owner_page"] for o in owners}
    assert len(registered)==len(owners),"Duplicate tracked Wiki page"
    extra={c["owner_page"] for c in claims}-registered
    if extra:
        raise ValueError(f"Claims cite owners outside the reviewed registry: {sorted(extra)}")
    claim_by_page={}
    for c in claims:
        claim_by_page.setdefault(c["owner_page"],[]).append(c)
    for o in owners:
        page=o["owner_page"]
        raw=raw_files[page]
        text=raw.decode("utf-8")
        sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        page_records=sections(page,text,sha)
        records.extend(page_records)
        low=text.lower()
        for c in claim_by_page.get(page,[]):
            anchor=c["wiki_source_anchor"].strip()
            if not anchor:
                missing.append(c["fact_id"]);continue
            pos=low.find(anchor.lower())
            if pos<0:
                missing.append(c["fact_id"]);continue
            if low.find(anchor.lower(),pos+len(anchor))>=0:
                ambiguous.append(c["fact_id"]);continue
            line=text.count("\n",0,pos)+1
            found=next((x for x in page_records
                        if x["start_line"]<=line<x["end_line_exclusive"]),None)
            if found is None:
                preamble.append(c["fact_id"])
            else:
                found["unique_claims"]+=1
    reached=sum(bool(r["unique_claims"]) for r in records)
    return {"owners":len(owners),"sections":len(records),
            "sections_with_a_unique_claim":reached,
            "section_coverage_percent":round(100*reached/len(records),2) if records else 0,
            "claims":len(claims),"stale_claims":missing,"ambiguous_claims":ambiguous,
            "preamble_claims":preamble,
            "warning":"Section anchor coverage is NOT exhaustive semantic migration."},records

def self_test():
    owner=[{"owner_page":"A.md"},{"owner_page":"B.md"}]
    fact=[{"fact_id":"A1","owner_page":"A.md","wiki_source_anchor":"unique marker"},
          {"fact_id":"A2","owner_page":"A.md","wiki_source_anchor":"repeated marker"},
          {"fact_id":"A3","owner_page":"A.md","wiki_source_anchor":"absent marker"},
          {"fact_id":"B1","owner_page":"B.md","wiki_source_anchor":"second unique"}]
    raw={"A.md":b"# A\n## One\nunique marker\n### Two\nrepeated marker\n## Three\nrepeated marker\n",
         "B.md":b"# B\n## Four\nsecond unique\n"}
    result,sections_=analyze(owner,fact,raw)
    assert (result["owners"],result["sections"],result["sections_with_a_unique_claim"])==(2,4,2)
    assert result["stale_claims"]==["A3"]
    assert result["ambiguous_claims"]==["A2"]
    assert len({r["source_blob_sha"] for r in sections_})==2
    print("Section-census self-test passed: unique, duplicate and absent anchors distinguished.")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir",type=Path,help="Current MKMSZ-Randomizer/wiki checkout (required for live audit)")
    parser.add_argument("--csv",type=Path,help="Optional section-by-section TSV output")
    parser.add_argument("--json",type=Path,help="Optional machine-readable summary output")
    parser.add_argument("--self-test",action="store_true",help="Run synthetic fixture, no Wiki checkout needed")
    args=parser.parse_args()
    if args.self_test:
        self_test();return
    if args.wiki_dir is None:
        parser.error("--wiki-dir required for a live audit; use --self-test to verify script")
    owners=tsv("known_knowledge_owners.tsv")
    claims=tsv("known_knowledge_claims.tsv")
    missing=[r["owner_page"] for r in owners if not (args.wiki_dir/r["owner_page"]).is_file()]
    if missing:
        parser.error(f"Missing {len(missing)} Wiki owners: {missing}")
    raw={r["owner_page"]:(args.wiki_dir/r["owner_page"]).read_bytes() for r in owners}
    result,sections_=analyze(owners,claims,raw)
    print(f"{result['owners']} tracked owners / {result['sections']} real Wiki headings.")
    print(f"{result['sections_with_a_unique_claim']}/{result['sections']} headings "
          f"have at least one uniquely located known claim ({result['section_coverage_percent']}%).")
    print(f"{len(result['stale_claims'])} stale and "
          f"{len(result['ambiguous_claims'])} ambiguous claim anchors; "
          f"{len(result['preamble_claims'])} claims in pre-heading introductions.")
    print(result["warning"])
    if args.csv:
        args.csv.parent.mkdir(parents=True,exist_ok=True)
        with args.csv.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(sections_[0]))
            writer.writeheader();writer.writerows(sections_)
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
