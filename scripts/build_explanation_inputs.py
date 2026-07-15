#!/usr/bin/env python3
"""
Build inputs for the fraud explanation step.

This script uses the scored transaction sample from the original fraud project.
It picks high-risk transactions and prepares the information needed to write a
short explanation for a fraud analyst.

Default input:
  data/sample/scored_transactions_sample.csv
  data/processed/threshold_analysis.csv

Output:
  reports/llm_explanations/explanation_input_sample.csv
"""

from pathlib import Path
import argparse
import pandas as pd
import numpy as np


SCORE_NAMES = [
    "fraud_score", "risk_score", "score", "probability",
    "predicted_probability", "fraud_probability", "model_score",
    "random_forest_score", "random_forest_probability"
]
AMOUNT_NAMES = ["Amount", "amount", "transaction_amount"]
LABEL_NAMES = ["Class", "class", "true_label", "label", "is_fraud"]


def find_column(df, possible_names):
    lower_cols = {c.lower(): c for c in df.columns}
    for name in possible_names:
        if name.lower() in lower_cols:
            return lower_cols[name.lower()]
    return None


def find_score_column(df):
    score_col = find_column(df, SCORE_NAMES)
    if score_col:
        return score_col

    # backup: find a numeric column that looks like a probability
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) > 0 and s.between(0, 1).mean() > 0.95 and s.nunique() > 10:
            return col

    raise ValueError(
        "I could not find the model score column. Rename it to fraud_score, risk_score, or model_score."
    )


def pick_threshold(threshold_file, default_threshold):
    if not threshold_file.exists():
        return default_threshold, f"Used default threshold {default_threshold:.2f}."

    table = pd.read_csv(threshold_file)
    threshold_col = next((c for c in table.columns if "threshold" in c.lower() or "cutoff" in c.lower()), None)

    if threshold_col is None or table.empty:
        return default_threshold, f"Used default threshold {default_threshold:.2f}."

    precision_col = next((c for c in table.columns if "precision" in c.lower()), None)
    recall_col = next((c for c in table.columns if "recall" in c.lower()), None)

    if precision_col and recall_col:
        temp = table.copy()
        temp["f1"] = 2 * temp[precision_col] * temp[recall_col] / (
            temp[precision_col] + temp[recall_col] + 1e-12
        )
        row = temp.sort_values("f1", ascending=False).iloc[0]
        return float(row[threshold_col]), "Used the threshold with the best precision-recall balance."

    row = table.iloc[len(table) // 2]
    return float(row[threshold_col]), "Used a middle threshold from the threshold analysis table."


def make_risk_note(row, score_col, amount_col, threshold):
    notes = [
        f"model score {row[score_col]:.3f} is above threshold {threshold:.2f}"
    ]

    if amount_col is not None and pd.notna(row.get(amount_col)):
        notes.append(f"transaction amount is {float(row[amount_col]):.2f}")

    # The Kaggle fraud dataset uses anonymized V1-V28 features, so I only refer to them as anonymized signals.
    v_cols = [c for c in row.index if str(c).startswith("V") and str(c)[1:].isdigit()]
    if v_cols:
        top = sorted(v_cols, key=lambda c: abs(float(row[c])) if pd.notna(row[c]) else 0, reverse=True)[:3]
        notes.append("large anonymized feature values: " + ", ".join([f"{c}={float(row[c]):.2f}" for c in top]))

    notes.append("no merchant, identity, or location details are used")
    return "; ".join(notes)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scored", default="data/sample/scored_transactions_sample.csv")
    parser.add_argument("--thresholds", default="data/processed/threshold_analysis.csv")
    parser.add_argument("--outdir", default="reports/llm_explanations")
    parser.add_argument("--threshold", type=float, default=0.30)
    parser.add_argument("--top-n", type=int, default=50)
    args = parser.parse_args()

    scored_file = Path(args.scored)
    threshold_file = Path(args.thresholds)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(scored_file)

    score_col = find_score_column(df)
    amount_col = find_column(df, AMOUNT_NAMES)
    label_col = find_column(df, LABEL_NAMES)

    threshold, threshold_note = pick_threshold(threshold_file, args.threshold)

    df = df.copy()
    df["transaction_id"] = df["transaction_id"] if "transaction_id" in df.columns else df.index
    df["fraud_score_for_explanation"] = df[score_col].astype(float)
    df["selected_threshold"] = threshold
    df["review_decision"] = np.where(df["fraud_score_for_explanation"] >= threshold, "Review", "Pass")

    flagged = df[df["review_decision"] == "Review"].copy()
    if flagged.empty:
        flagged = df.sort_values("fraud_score_for_explanation", ascending=False).head(args.top_n).copy()
        flagged["review_decision"] = "Review"
    else:
        flagged = flagged.sort_values("fraud_score_for_explanation", ascending=False).head(args.top_n).copy()

    flagged["risk_notes"] = flagged.apply(
        lambda row: make_risk_note(row, score_col, amount_col, threshold),
        axis=1
    )
    flagged["threshold_note"] = threshold_note

    keep_cols = ["transaction_id"]
    if amount_col:
        keep_cols.append(amount_col)
    keep_cols += [
        score_col,
        "fraud_score_for_explanation",
        "selected_threshold",
        "review_decision",
        "risk_notes",
        "threshold_note",
    ]
    if label_col:
        keep_cols.append(label_col)

    output = flagged[keep_cols]
    output_file = outdir / "explanation_input_sample.csv"
    output.to_csv(output_file, index=False)

    print(f"Saved {len(output)} rows to {output_file}")
    print(f"Score column used: {score_col}")
    print(f"Threshold used: {threshold:.3f}")


if __name__ == "__main__":
    main()
