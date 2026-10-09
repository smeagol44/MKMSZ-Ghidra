#!/usr/bin/env python3
"""Validate every documented Function Registry address against appropriate Ghidra navigation.

Function definitions, scoped overlay functions, internal labels, code comments and
bookmarks are distinct; a navigable address is not necessarily a function entry.
"""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def read(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))
registry=read("function_registry_crosswalk.tsv")
claims={x["fact_id"]:x for x in read("known_knowledge_claims.tsv")}
funs={x["address"].lower() for x in read("functions.tsv")}
overlay={(x["scope"],x["address"].lower()) for x in read("overlay_functions.tsv")}
labels={(x["scope"],x["address"].lower()) for x in read("code_labels.tsv")}
books={(x["scope"],x["address"].lower()) for x in read("bookmarks.tsv")}
notes={(x["scope"],x["address"].lower()) for x in read("comments.tsv")}
assert len(registry)==len({r["registry_id"] for r in registry})==166
annotation_rows=0
for r in registry:
    key=r["registry_id"]
    scope=r["scope"]
    addrs=r["addresses"].split(",")
    kinds=[]
    for a in addrs:
        kind=("function" if scope=="global" and a in funs else
              "overlay-function" if (scope,a) in overlay else
              "internal-label" if (scope,a) in labels else
              "bookmark" if (scope,a) in books else
              "comment" if (scope,a) in notes else "")
        assert kind, (key,a)
        kinds.append(kind)
    assert r["navigation_sources"]==",".join(f"{a}:{k}" for a,k in zip(addrs,kinds))
    assert r["indexed_addresses"]==r["addresses"]
    assert not r["unindexed_addresses"]
    assert r["address_index_status"]=="all-addresses-indexed"
    if any(kind in ("bookmark","comment") for kind in kinds):
        annotation_rows+=1
    assert claims[key]["migration_status"]=="ghidra-confirmed"
    assert claims[key]["target_path"].startswith("analysis/")
assert annotation_rows>=22
print(f"166/166 known Function Registry rows have full scoped address navigation; "
      f"{annotation_rows} rows use existing bookmarks/comments. No function identities inferred.")
