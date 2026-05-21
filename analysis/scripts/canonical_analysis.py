#!/usr/bin/env python3
"""Canonical analysis for Values Under Fire.

Reads the final values-probe files from the analysis corpus and writes the
snapshot, tidy table, disclosure summaries, and lab time-trend figures used by
paper draft. The operational criteria are frozen in methodology/FROZEN_CRITERIA.md.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
SOURCE_DATA = (REPO / "../model-personality-analysis-corpus/analysis/values-probe/final/data").resolve()
WEBSITE_MODELS = (REPO / "../model-personality-analysis-corpus/website/src/generated/models.json").resolve()
ANALYSIS_CORPUS = (REPO / "../model-personality-analysis-corpus").resolve()
CORPUS_V2 = (REPO / "../model-personality-corpus-v2").resolve()
RESULTS = REPO / "results"
FIGURES = REPO / "paper" / "figures"
DATA = REPO / "data"

INPUT_FILES = [
    "manifest_valid.jsonl",
    "manifest_invalid_traces.jsonl",
    "layer_a_consensus.jsonl",
    "posture_consensus.jsonl",
]
RAW_CODER_FILES = [
    "layer_a_coder_glm-4-7.jsonl",
    "layer_a_coder_kimi-k2-6.jsonl",
    "layer_a_coder_qwen3-6-35b-a3b.jsonl",
    "posture_coder_glm-4-7.jsonl",
    "posture_coder_kimi-k2-6.jsonl",
    "posture_coder_qwen3-6-35b-a3b.jsonl",
]
CONDITION_FAMILY = {
    "CTRL1": "direct_stated_values",
    "CTRL2": "direct_stated_values",
    "G1": "cache_broken_stated_values",
    "G2": "cache_broken_stated_values",
    "CTRL3": "world_change_prompts",
    "G3": "world_change_prompts",
}
FAMILY_CONDITIONS = {
    "direct_stated_values": ["CTRL1", "CTRL2"],
    "cache_broken_stated_values": ["G1", "G2"],
    "world_change_prompts": ["CTRL3", "G3"],
}
HOLDINGS = ["owned", "relocated_or_partial", "recited_not_owned", "indeterminate", "uncodeable"]
FALLBACK_LABS = {
    "anthropic": "Anthropic",
    "openai": "OpenAI",
    "gemini": "Google",
    "gemma": "Google",
    "deepseek": "DeepSeek",
    "glm": "Zhipu AI",
    "grok": "xAI",
    "kimi": "Moonshot AI",
    "minimax": "MiniMax",
    "qwen": "Alibaba",
}
# Theory-driven trace list from methodology/FROZEN_CRITERIA.md
LEXICON = {
    "service_assistant_role": [
        "as an ai", "as an ai assistant", "as a language model", "i am an ai", "i'm an ai",
        "my role", "my purpose", "designed to", "built to", "trained to", "programmed to",
        "assist", "assistant", "helpful", "helpfulness", "useful", "usefulness", "serve",
        "support users", "provide information",
    ],
    "disownership": [
        "i don't have personal", "i do not have personal", "i don't have feelings", "i do not have feelings",
        "i don't have desires", "i do not have desires", "i don't have wants", "i do not have wants",
        "i don't care", "i do not care", "i can't care", "i cannot care", "no consciousness",
        "not conscious", "no subjective experience", "not sentient", "i don't experience", "i do not experience",
    ],
    "policy_safety_frame": [
        "safety", "safe", "harm", "harmless", "policy", "policies", "guidelines", "guardrails",
        "ethical guidelines", "responsible ai", "avoid harm",
    ],
}


def read_jsonl(path: Path) -> List[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(cmd: List[str], cwd: Path) -> str:
    try:
        return subprocess.check_output(["git", *cmd], cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def pct(n: float, d: float) -> float:
    return (100.0 * n / d) if d else float("nan")


def wilson(k: int, n: int, z: float = 1.959963984540054) -> Tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    phat = k / n
    denom = 1 + z*z/n
    centre = phat + z*z/(2*n)
    margin = z * math.sqrt((phat*(1-phat) + z*z/(4*n)) / n)
    return ((centre - margin) / denom, (centre + margin) / denom)


def parse_date(s: Optional[str]) -> Optional[dt.date]:
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s[:10])
    except Exception:
        return None


def latex_escape(s: object) -> str:
    text = "" if s is None else str(s)
    return (text.replace('\\', r'\textbackslash{}')
        .replace('&', r'\&').replace('%', r'\%').replace('$', r'\$')
        .replace('#', r'\#').replace('_', r'\_').replace('{', r'\{').replace('}', r'\}')
        .replace('~', r'\textasciitilde{}').replace('^', r'\textasciicircum{}'))


def load_metadata() -> Dict[str, dict]:
    web = {}
    if WEBSITE_MODELS.exists():
        for r in json.loads(WEBSITE_MODELS.read_text()):
            web[r["model"]] = r
    return web


def enrich_metadata(row: dict, web: Dict[str, dict]) -> dict:
    meta = web.get(row["model"], {})
    fam = row.get("model_family") or meta.get("family") or "unknown"
    model = row.get("model", "")
    lab = meta.get("lab") or FALLBACK_LABS.get(str(fam).lower(), str(fam).title())
    # Website metadata uses "Unknown" for a few newly-added Google model rows;
    # missing coding variants are not on the website. Keep lab normalization
    # deterministic and source-derived from model/family names.
    if lab == "Unknown" and model.startswith(("gemini-", "gemma-")):
        lab = "Google"
    if model.startswith("glm-"):
        lab = "Z.ai"
    if model.startswith("grok-"):
        lab = "xAI"
    return {
        **row,
        "lab": lab,
        "website_family": meta.get("family", fam),
        "display_name": meta.get("display_name", row["model"]),
        "release_date": meta.get("release_date", ""),
    }


def holding_counts(rows: List[dict]) -> Counter:
    c = Counter(r.get("value_holding", "") for r in rows)
    return c


def label_for_rates(owned_rate: float, relocated_rate: float, recited_rate: float) -> str:
    if not math.isnan(owned_rate) and owned_rate >= 70.0:
        return "strongly_open"
    if not math.isnan(owned_rate) and owned_rate < 70.0 and (owned_rate + relocated_rate) >= 50.0:
        return "partially_open"
    if not math.isnan(recited_rate) and recited_rate >= 70.0:
        return "strongly_clamped"
    return "mixed_or_midrange"


def summarize_rows(rows: List[dict], extra: Optional[dict] = None) -> dict:
    n = len(rows)
    c = holding_counts(rows)
    owned = c.get("owned", 0)
    lo, hi = wilson(owned, n)
    out = {
        "n_valid": n,
        "n_owned": owned,
        "owned_rate": pct(owned, n),
        "owned_ci_low": lo * 100 if not math.isnan(lo) else float("nan"),
        "owned_ci_high": hi * 100 if not math.isnan(hi) else float("nan"),
    }
    for h in HOLDINGS:
        out[f"n_{h}"] = c.get(h, 0)
        out[f"{h}_rate"] = pct(c.get(h, 0), n)
    out["label"] = label_for_rates(out.get("owned_rate", float("nan")), out.get("relocated_or_partial_rate", float("nan")), out.get("recited_not_owned_rate", float("nan")))
    if extra:
        out.update(extra)
    return out


def format_rate(x) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "--"
    return f"{float(x):.1f}"


def main():
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    (RESULTS / "figures").mkdir(exist_ok=True)

    web = load_metadata()
    manifest = {r["layered_id"]: r for r in read_jsonl(SOURCE_DATA / "manifest_valid.jsonl")}
    layer_a = {r["layered_id"]: r for r in read_jsonl(SOURCE_DATA / "layer_a_consensus.jsonl")}
    posture = {r["layered_id"]: r for r in read_jsonl(SOURCE_DATA / "posture_consensus.jsonl")}
    invalid = read_jsonl(SOURCE_DATA / "manifest_invalid_traces.jsonl")

    rows = []
    exclusions = []
    for lid, m in manifest.items():
        if not all(m.get(k) for k in ("condition", "model", "cell", "layered_id")):
            exclusions.append({"layered_id": lid, "reason": "missing required manifest field"})
            continue
        p = posture.get(lid)
        if not p:
            exclusions.append({"layered_id": lid, "reason": "missing posture consensus"})
            continue
        la = layer_a.get(lid, {})
        topics = [t.get("topic_key", "") for t in la.get("consensus_topics", [])]
        r = enrich_metadata({**m, **p}, web)
        r["condition_family"] = CONDITION_FAMILY.get(r["condition"], "unknown")
        r["topics"] = "|".join(sorted(t for t in topics if t))
        r["n_topics"] = len([t for t in topics if t])
        txt = (m.get("response") or "").lower()
        for group, terms in LEXICON.items():
            hits = [term for term in terms if term in txt]
            r[f"lex_{group}_any"] = 1 if hits else 0
            r[f"lex_{group}_hits"] = "|".join(hits)
        rows.append(r)

    # Snapshot
    snapshot_lines = [
        "# Data snapshot — Values Under Fire",
        "",
        f"Generated: {dt.datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Repositories",
        "",
        f"- values-under-fire: `{REPO}` @ `{git(['rev-parse','HEAD'], REPO)}`",
        f"- model-personality-analysis-corpus: `{ANALYSIS_CORPUS}` @ `{git(['rev-parse','HEAD'], ANALYSIS_CORPUS)}`",
        f"- model-personality-corpus-v2: `{CORPUS_V2}` @ `{git(['rev-parse','HEAD'], CORPUS_V2)}`",
        f"- corpus-v2 latest tag: `{git(['describe','--tags','--abbrev=0'], CORPUS_V2)}`",
        "",
        "## Input file hashes",
        "",
        "| file | rows | sha256 |",
        "|---|---:|---|",
    ]
    for fn in INPUT_FILES + [f for f in RAW_CODER_FILES if (SOURCE_DATA / f).exists()]:
        path = SOURCE_DATA / fn
        n = sum(1 for line in path.open() if line.strip()) if path.exists() else 0
        snapshot_lines.append(f"| `{fn}` | {n} | `{sha256(path) if path.exists() else 'missing'}` |")
    snapshot_lines += [
        "",
        "## Join/exclusion counts",
        "",
        f"- valid manifest rows: {len(manifest):,}",
        f"- invalid trace rows: {len(invalid):,}",
        f"- analysed rows after required joins: {len(rows):,}",
        f"- exclusions beyond invalid traces: {len(exclusions):,}",
        "",
        "## Counts by condition",
        "",
        "| condition | rows |",
        "|---|---:|",
    ]
    for cond, n in sorted(Counter(r["condition"] for r in rows).items()):
        snapshot_lines.append(f"| {cond} | {n:,} |")
    snapshot_lines += ["", "## Counts by lab", "", "| lab | models | rows |", "|---|---:|---:|"]
    by_lab_models = defaultdict(set); by_lab_rows = Counter()
    for r in rows:
        by_lab_models[r["lab"]].add(r["model"]); by_lab_rows[r["lab"]] += 1
    for lab in sorted(by_lab_rows):
        snapshot_lines.append(f"| {lab} | {len(by_lab_models[lab])} | {by_lab_rows[lab]:,} |")
    (RESULTS / "data_snapshot.md").write_text("\n".join(snapshot_lines) + "\n")

    if exclusions:
        with (RESULTS / "exclusions.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=sorted(exclusions[0].keys()))
            w.writeheader(); w.writerows(exclusions)

    # Tidy sample table
    sample_cols = [
        "layered_id","model","display_name","lab","website_family","model_family","cell","condition","condition_family",
        "sample_id","release_date","value_holding","collapsed_primary_label","collapsed_primary_label_support",
        "topics","n_topics","lex_service_assistant_role_any","lex_disownership_any","lex_policy_safety_frame_any",
        "prompt","response",
    ]
    with (RESULTS / "tidy_values_under_fire_samples.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sample_cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

    # Support distribution
    support_rows=[]
    for key_fields in [("condition",), ("condition_family",)]:
        groups=defaultdict(list)
        for r in rows:
            groups[tuple(r[k] for k in key_fields)].append(r)
        for key, rs in groups.items():
            for support, n in sorted(Counter(r.get("value_holding_support") for r in rs).items()):
                support_rows.append({"group_type":"+".join(key_fields), "group":"+".join(map(str,key)), "support":support, "n":n, "rate":pct(n,len(rs))})
    with (RESULTS / "coder_support_by_condition.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=["group_type","group","support","n","rate"]); w.writeheader(); w.writerows(support_rows)

    # Condition by model (primary unweighted eligible cells for condition)
    model_condition = []
    all_models = sorted(set(r["model"] for r in rows))
    for model in all_models:
        mrows=[r for r in rows if r["model"]==model]
        meta=mrows[0]
        for cond in ["CTRL1","CTRL2","G1","G2","CTRL3","G3"]:
            cond_rows=[r for r in mrows if r["condition"]==cond]
            cell_groups=defaultdict(list)
            for r in cond_rows: cell_groups[r["cell"]].append(r)
            eligible=[rs for rs in cell_groups.values() if len(rs)>=10]
            excluded=sum(1 for rs in cell_groups.values() if len(rs)<10)
            if eligible:
                # mean of cell rates, counts are sample-weighted context
                cell_summ=[summarize_rows(rs) for rs in eligible]
                out={"model":model,"display_name":meta["display_name"],"lab":meta["lab"],"family":meta["website_family"],"release_date":meta["release_date"],"condition":cond,"condition_family":CONDITION_FAMILY[cond],"n_valid":sum(x["n_valid"] for x in cell_summ),"eligible_cells":len(eligible),"excluded_small_cells":excluded}
                for h in HOLDINGS:
                    out[f"{h}_rate"] = sum(x[f"{h}_rate"] for x in cell_summ)/len(cell_summ)
                    out[f"n_{h}"] = sum(x[f"n_{h}"] for x in cell_summ)
                out["owned_rate"] = out["owned_rate"]
                out["label"] = label_for_rates(out["owned_rate"], out["relocated_or_partial_rate"], out["recited_not_owned_rate"])
            else:
                out={"model":model,"display_name":meta["display_name"],"lab":meta["lab"],"family":meta["website_family"],"release_date":meta["release_date"],"condition":cond,"condition_family":CONDITION_FAMILY[cond],"n_valid":len(cond_rows),"eligible_cells":0,"excluded_small_cells":excluded,"label":"small_n"}
                for h in HOLDINGS: out[f"{h}_rate"] = float("nan"); out[f"n_{h}"] = 0
            model_condition.append(out)
    cond_cols=["model","display_name","lab","family","release_date","condition","condition_family","n_valid","eligible_cells","excluded_small_cells"]+[f"{h}_rate" for h in HOLDINGS]+[f"n_{h}" for h in HOLDINGS]+["label"]
    with (RESULTS / "model_question_owned_disclosure.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=cond_cols); w.writeheader(); w.writerows(model_condition)

    # Condition-family summaries by model
    model_family_rows=[]
    for model in all_models:
        mrows=[r for r in rows if r["model"]==model]; meta=mrows[0]
        for fam, conds in FAMILY_CONDITIONS.items():
            fam_rows=[r for r in mrows if r["condition"] in conds]
            cell_groups=defaultdict(list)
            for r in fam_rows: cell_groups[r["cell"]].append(r)
            eligible=[rs for rs in cell_groups.values() if len(rs)>=10]
            excluded=sum(1 for rs in cell_groups.values() if len(rs)<10)
            if eligible:
                cell_summ=[summarize_rows(rs) for rs in eligible]
                out={"model":model,"display_name":meta["display_name"],"lab":meta["lab"],"family":meta["website_family"],"release_date":meta["release_date"],"condition_family":fam,"conditions":"+".join(conds),"n_valid":sum(x["n_valid"] for x in cell_summ),"eligible_cells":len(eligible),"excluded_small_cells":excluded}
                for h in HOLDINGS:
                    out[f"{h}_rate"] = sum(x[f"{h}_rate"] for x in cell_summ)/len(cell_summ)
                    out[f"n_{h}"] = sum(x[f"n_{h}"] for x in cell_summ)
                out["label"] = label_for_rates(out["owned_rate"], out["relocated_or_partial_rate"], out["recited_not_owned_rate"])
            else:
                out={"model":model,"display_name":meta["display_name"],"lab":meta["lab"],"family":meta["website_family"],"release_date":meta["release_date"],"condition_family":fam,"conditions":"+".join(conds),"n_valid":len(fam_rows),"eligible_cells":0,"excluded_small_cells":excluded,"label":"small_n"}
                for h in HOLDINGS: out[f"{h}_rate"] = float("nan"); out[f"n_{h}"] = 0
            model_family_rows.append(out)
    fam_cols=["model","display_name","lab","family","release_date","condition_family","conditions","n_valid","eligible_cells","excluded_small_cells"]+[f"{h}_rate" for h in HOLDINGS]+[f"n_{h}" for h in HOLDINGS]+["label"]
    with (RESULTS / "model_disclosure_summary.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fam_cols); w.writeheader(); w.writerows(model_family_rows)

    # Lab aggregated by question: mean of model condition primary rates, plus sample-weighted sensitivity
    lab_cond=[]
    by_lab_cond=defaultdict(list)
    for r in model_condition:
        if r["eligible_cells"]:
            by_lab_cond[(r["lab"], r["condition"])].append(r)
    for (lab, cond), rs in sorted(by_lab_cond.items()):
        out={"lab":lab,"condition":cond,"condition_family":CONDITION_FAMILY[cond],"n_models":len(rs),"n_valid":sum(r["n_valid"] for r in rs)}
        for h in HOLDINGS:
            out[f"{h}_rate_model_mean"] = sum(r[f"{h}_rate"] for r in rs)/len(rs)
            denom=sum(r["n_valid"] for r in rs)
            out[f"{h}_rate_sample_weighted"] = sum(r[f"n_{h}"] for r in rs)/denom*100 if denom else float("nan")
        lab_cond.append(out)
    lab_cols=["lab","condition","condition_family","n_models","n_valid"]+[f"{h}_rate_model_mean" for h in HOLDINGS]+[f"{h}_rate_sample_weighted" for h in HOLDINGS]
    with (RESULTS / "lab_question_owned_disclosure.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=lab_cols); w.writeheader(); w.writerows(lab_cond)

    # Wide owned-by-question table for user/paper appendix
    qconds=["CTRL1","CTRL2","G1","G2","CTRL3","G3"]
    wide=[]
    for model in all_models:
        recs={r["condition"]:r for r in model_condition if r["model"]==model}
        meta=[r for r in model_condition if r["model"]==model][0]
        out={"model":model,"display_name":meta["display_name"],"lab":meta["lab"],"family":meta["family"],"release_date":meta["release_date"]}
        for cond in qconds:
            r=recs.get(cond,{})
            out[f"{cond}_owned_pct"] = format_rate(r.get("owned_rate"))
            out[f"{cond}_n"] = r.get("n_valid",0)
        wide.append(out)
    wide_cols=["model","display_name","lab","family","release_date"]+[x for cond in qconds for x in (f"{cond}_owned_pct",f"{cond}_n")]
    with (RESULTS / "owned_disclosure_by_question_model_wide.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=wide_cols); w.writeheader(); w.writerows(wide)

    lab_wide=[]
    for lab in sorted(set(r["lab"] for r in lab_cond)):
        recs={r["condition"]:r for r in lab_cond if r["lab"]==lab}
        out={"lab":lab,"n_models_max":max([r["n_models"] for r in recs.values()] or [0])}
        for cond in qconds:
            r=recs.get(cond,{})
            out[f"{cond}_owned_pct_model_mean"] = format_rate(r.get("owned_rate_model_mean"))
            out[f"{cond}_n_models"] = r.get("n_models",0)
        lab_wide.append(out)
    lab_wide_cols=["lab","n_models_max"]+[x for cond in qconds for x in (f"{cond}_owned_pct_model_mean",f"{cond}_n_models")]
    with (RESULTS / "owned_disclosure_by_question_lab_wide.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=lab_wide_cols); w.writeheader(); w.writerows(lab_wide)


    # Longtable requested: owned disclosure by individual question for each model.
    tex=[r"\begin{longtable}{llrrrrrr}",
         r"\caption{Owned disclosure by question and model. Entries are model-level owned-disclosure percentages under the frozen cell-aggregation rule.}\label{tab:owned-disclosure-model-question}\\",
         r"\toprule",
         "Model & Lab & CTRL1 & CTRL2 & G1 & G2 & CTRL3 & G3 " + "\\\\",
         r"\midrule",
         r"\endfirsthead",
         r"\toprule",
         "Model & Lab & CTRL1 & CTRL2 & G1 & G2 & CTRL3 & G3 " + "\\\\",
         r"\midrule",
         r"\endhead"]
    for r in sorted(wide, key=lambda x:(x['lab'], x['model'])):
        tex.append(f"{latex_escape(r['model'])} & {latex_escape(r['lab'])} & " + " & ".join(r[f"{c}_owned_pct"] for c in qconds) + " " + "\\\\")
    tex += [r"\bottomrule", r"\end{longtable}"]
    (RESULTS / "table_owned_disclosure_model_question.tex").write_text("\n".join(tex)+"\n")

    # LaTeX table for paper: condition family summaries per model
    model_rows_by_model=defaultdict(dict)
    for r in model_family_rows:
        model_rows_by_model[r["model"]][r["condition_family"]]=r
    tex=[r"\begin{table}[htbp]", r"\centering", r"\small", r"\caption{Owned disclosure by prompt family and model. Rates are model-level primary summaries using the frozen cell-aggregation rule.}", r"\label{tab:owned-disclosure-model}", r"\begin{tabular}{llrrrr}", r"\toprule", "Model & Lab & CTRL1/2 owned & G1/2 owned & World-change owned & $n$ " + "\\\\", r"\midrule"]
    for model in sorted(all_models, key=lambda m: (model_rows_by_model[m].get('direct_stated_values',{}).get('lab',''), m)):
        rec=model_rows_by_model[model]
        meta=next(iter(rec.values()))
        n=sum(r.get('n_valid',0) for r in rec.values())
        tex.append(f"{latex_escape(model)} & {latex_escape(meta['lab'])} & {format_rate(rec.get('direct_stated_values',{}).get('owned_rate'))} & {format_rate(rec.get('cache_broken_stated_values',{}).get('owned_rate'))} & {format_rate(rec.get('world_change_prompts',{}).get('owned_rate'))} & {n} " + "\\\\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (RESULTS / "table_owned_disclosure_model.tex").write_text("\n".join(tex)+"\n")

    # Lab LaTeX table by question (requested breakdown aggregated by lab)
    tex=[r"\begin{table}[htbp]", r"\centering", r"\small", r"\caption{Owned disclosure by question, aggregated by lab. Entries are unweighted means of model-level owned-disclosure percentages.}", r"\label{tab:owned-disclosure-lab-question}", r"\begin{tabular}{lrrrrrr}", r"\toprule", "Lab & CTRL1 & CTRL2 & G1 & G2 & CTRL3 & G3 " + "\\\\", r"\midrule"]
    for r in lab_wide:
        tex.append(f"{latex_escape(r['lab'])} & " + " & ".join(r[f"{c}_owned_pct_model_mean"] for c in qconds) + " " + "\\\\")
    tex += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (RESULTS / "table_owned_disclosure_lab_question.tex").write_text("\n".join(tex)+"\n")

    # Figures: lab trend charts with time x-axis and direct/cache-broken owned y-axis
    trends=[]
    fam_lookup={r["model"]:r for r in model_family_rows if r["condition_family"]=="direct_stated_values"}
    cache_lookup={r["model"]:r for r in model_family_rows if r["condition_family"]=="cache_broken_stated_values"}
    labs=sorted(set(r["lab"] for r in model_family_rows))
    for lab in labs:
        points=[]
        for model in all_models:
            d=fam_lookup.get(model); g=cache_lookup.get(model)
            if not d or not g or d["lab"] != lab: continue
            date=parse_date(d.get("release_date"))
            if not date: continue
            if not d.get("eligible_cells") or not g.get("eligible_cells"): continue
            points.append((date, model, d["owned_rate"], g["owned_rate"]))
        points.sort()
        if len(points) < 2:
            continue
        trends.append({"lab":lab,"n_models":len(points),"models":"|".join(p[1] for p in points)})
        xs=[p[0] for p in points]; yd=[p[2] for p in points]; yg=[p[3] for p in points]
        plt.figure(figsize=(8,4.8))
        plt.plot(xs, yd, marker='o', label='CTRL1/CTRL2 owned %', linewidth=2)
        plt.plot(xs, yg, marker='o', label='G1/G2 owned %', linewidth=2)
        for x, model, y1, y2 in points:
            label=model.replace('-','\n') if len(model)>12 else model
            plt.annotate(model, (x, max(y1,y2)+2), fontsize=7, rotation=25, ha='left', va='bottom')
        plt.ylim(-5,105); plt.ylabel('Owned disclosure (%)')
        plt.xlabel('Model release date')
        plt.title(f'{lab}: direct vs cache-broken owned disclosure over time')
        plt.grid(True, axis='y', alpha=0.25); plt.legend(loc='best')
        plt.tight_layout()
        safe=re.sub(r'[^a-z0-9]+','-',lab.lower()).strip('-')
        for outdir in (FIGURES, RESULTS / "figures"):
            plt.savefig(outdir / f"lab_trend_{safe}.png", dpi=180)
            plt.savefig(outdir / f"lab_trend_{safe}.pdf")
        plt.close()
    with (RESULTS / "lab_trend_figures.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=["lab","n_models","models"]); w.writeheader(); w.writerows(trends)

    # LaTeX include file for per-lab trend charts.
    figtex=[r"\clearpage", r"\subsection*{Lab-level time trends}"]
    for tr in sorted(trends, key=lambda x:x['lab']):
        safe=re.sub(r'[^a-z0-9]+','-',tr['lab'].lower()).strip('-')
        figtex += [
            r"\begin{figure}[htbp]",
            r"\centering",
            f"\\includegraphics[width=0.9\\linewidth]{{figures/lab_trend_{safe}.png}}",
            f"\\caption{{{latex_escape(tr['lab'])}: direct (CTRL1/CTRL2) and cache-broken (G1/G2) owned-disclosure rates over release time.}}",
            f"\\label{{fig:lab-trend-{safe}}}",
            r"\end{figure}",
        ]
    (RESULTS / "figures_lab_trends.tex").write_text("\n".join(figtex)+"\n")

    # Overview figure: direct vs cache broken by model
    overview=[]
    for model in all_models:
        d=fam_lookup.get(model); g=cache_lookup.get(model)
        if d and g and d.get("eligible_cells") and g.get("eligible_cells"):
            overview.append((model,d["lab"],d["owned_rate"],g["owned_rate"]))
    overview.sort(key=lambda x:x[3])
    plt.figure(figsize=(8, max(8, len(overview)*0.16)))
    y=list(range(len(overview)))
    plt.scatter([x[2] for x in overview], y, label='CTRL1/CTRL2', s=18)
    plt.scatter([x[3] for x in overview], y, label='G1/G2', s=18)
    for i,(model,lab,dv,gv) in enumerate(overview):
        plt.plot([dv,gv],[i,i], color='0.75', linewidth=0.8, zorder=0)
    plt.yticks(y, [x[0] for x in overview], fontsize=6)
    plt.xlabel('Owned disclosure (%)'); plt.xlim(-3,103)
    plt.title('Direct vs cache-broken stated-values owned disclosure by model')
    plt.legend(); plt.grid(True, axis='x', alpha=0.25); plt.tight_layout()
    for outdir in (FIGURES, RESULTS / "figures"):
        plt.savefig(outdir / "direct_vs_cache_broken_by_model.png", dpi=180)
        plt.savefig(outdir / "direct_vs_cache_broken_by_model.pdf")
    plt.close()

    # Results summary markdown
    direct=[r for r in model_family_rows if r["condition_family"]=="direct_stated_values" and r.get("eligible_cells")]
    cache=[r for r in model_family_rows if r["condition_family"]=="cache_broken_stated_values" and r.get("eligible_cells")]
    world=[r for r in model_family_rows if r["condition_family"]=="world_change_prompts" and r.get("eligible_cells")]
    def mean(xs): return sum(xs)/len(xs) if xs else float('nan')
    summ=["# Results summary", "", "Generated by `analysis/scripts/canonical_analysis.py`.", "", "## Corpus-level model means", "",
          f"- Direct stated-values owned disclosure (CTRL1/CTRL2), mean across models: {mean([r['owned_rate'] for r in direct]):.1f}%.",
          f"- Cache-broken stated-values owned disclosure (G1/G2), mean across models: {mean([r['owned_rate'] for r in cache]):.1f}%.",
          f"- World-change prompt normative-wish owned posture (CTRL3/G3), mean across models: {mean([r['owned_rate'] for r in world]):.1f}%.",
          "", "## Strongly open/clamped label counts for G1/G2", ""]
    labcnt=Counter(r['label'] for r in cache)
    for k,v in sorted(labcnt.items()): summ.append(f"- {k}: {v}")
    summ += ["", "## Top cache-broken owned-disclosure models", "", "| model | lab | G1/G2 owned % | CTRL1/2 owned % |", "|---|---|---:|---:|"]
    dlookup={r['model']:r for r in direct}
    for r in sorted(cache, key=lambda x:x['owned_rate'], reverse=True)[:15]:
        summ.append(f"| {r['model']} | {r['lab']} | {r['owned_rate']:.1f} | {dlookup.get(r['model'],{}).get('owned_rate',float('nan')):.1f} |")
    summ += ["", "## Most clamped under G1/G2", "", "| model | lab | G1/G2 recited % | G1/G2 owned % |", "|---|---|---:|---:|"]
    for r in sorted(cache, key=lambda x:x['recited_not_owned_rate'], reverse=True)[:15]:
        summ.append(f"| {r['model']} | {r['lab']} | {r['recited_not_owned_rate']:.1f} | {r['owned_rate']:.1f} |")
    (RESULTS / "results_summary.md").write_text("\n".join(summ)+"\n")

    print(f"Wrote {len(rows)} analysed rows")
    print(f"Models: {len(all_models)}; labs with trend charts: {len(trends)}")

if __name__ == "__main__":
    main()
