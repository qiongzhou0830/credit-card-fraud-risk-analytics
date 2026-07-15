#!/usr/bin/env python3
"""
Check whether the explanations stay close to the model output.

This is a simple check, not a perfect evaluator. The goal is to catch obvious
problems, like an explanation inventing a merchant, location, device, or user identity.
"""

from pathlib import Path
import argparse
import pandas as pd


FORBIDDEN_WORDS = [
    "merchant", "store", "retailer", "seller", "location", "country", "city",
    "cardholder", "identity", "device", "ip address", "browser",
    "purchase history", "past transactions", "bank account", "stolen card"
]


def get_explanation(row):
    llm_text = str(row.get("llm_explanation", "") or "").strip()
    if llm_text:
        return llm_text
    return str(row.get("template_explanation", "") or "").strip()


def review_explanation(row):
    text = get_explanation(row)
    lower = text.lower()

    forbidden_found = [w for w in FORBIDDEN_WORDS if w in lower]

    missing = []
    if "score" not in lower and "risk" not in lower:
        missing.append("score/risk")
    if "threshold" not in lower:
        missing.append("threshold")
    if str(row.get("review_decision", "")).lower() not in lower:
        missing.append("decision")

    ok = len(forbidden_found) == 0

    return pd.Series({
        "explanation_used": text,
        "looks_faithful": "yes" if ok else "check",
        "made_up_detail_risk": "yes" if forbidden_found else "no",
        "words_to_check": "; ".join(forbidden_found),
        "missing_context": "yes" if missing else "no",
        "missing_fields": "; ".join(missing),
        "my_notes": ""
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="reports/llm_explanations/analyst_explanations.csv")
    parser.add_argument("--outdir", default="reports/llm_explanations")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    review = df.apply(review_explanation, axis=1)

    base_cols = [
        "transaction_id",
        "fraud_score_for_explanation",
        "selected_threshold",
        "review_decision",
        "risk_notes"
    ]
    base_cols = [c for c in base_cols if c in df.columns]

    output = pd.concat([df[base_cols], review], axis=1)
    output.to_csv(outdir / "faithfulness_review.csv", index=False)

    summary = output[["looks_faithful", "made_up_detail_risk", "missing_context"]].apply(
        pd.Series.value_counts
    ).fillna(0).astype(int)
    summary.to_csv(outdir / "faithfulness_review_summary.csv")

    print(f"Saved review to {outdir / 'faithfulness_review.csv'}")
    print(summary)


if __name__ == "__main__":
    main()
