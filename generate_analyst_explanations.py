#!/usr/bin/env python3
"""
Generate simple analyst explanations.

This does not use an LLM to predict fraud.
The fraud model already created the score. This file only turns the score and
threshold decision into a short explanation that is easier to read.
"""

from pathlib import Path
import argparse
import pandas as pd


def make_prompt(row):
    return f"""Write a short explanation for a fraud analyst.

Use only the information below. Do not make up merchant, identity, location, device, or transaction history.

Transaction ID: {row.get('transaction_id')}
Amount: {row.get('Amount', row.get('amount', 'not provided'))}
Fraud score: {row.get('fraud_score_for_explanation')}
Threshold: {row.get('selected_threshold')}
Decision: {row.get('review_decision')}
Risk notes: {row.get('risk_notes')}
Threshold note: {row.get('threshold_note')}

Write 2 short sentences.
"""


def make_template_explanation(row):
    score = float(row["fraud_score_for_explanation"])
    threshold = float(row["selected_threshold"])
    decision = row["review_decision"]
    notes = row["risk_notes"]

    return (
        f"This transaction is marked as '{decision}' because its fraud score "
        f"({score:.3f}) is above the selected threshold ({threshold:.2f}). "
        f"The available signals are: {notes}. Since the data is anonymized, I do not infer details like merchant, identity, or location."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="reports/llm_explanations/explanation_input_sample.csv")
    parser.add_argument("--outdir", default="reports/llm_explanations")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    df["prompt_for_optional_llm"] = df.apply(make_prompt, axis=1)
    df["template_explanation"] = df.apply(make_template_explanation, axis=1)

    # If I later paste real LLM outputs, I can put them in this column.
    df["llm_explanation"] = ""

    df.to_csv(outdir / "analyst_explanations.csv", index=False)
    df[["transaction_id", "prompt_for_optional_llm"]].to_csv(outdir / "llm_prompts_for_review.csv", index=False)

    print(f"Saved explanations to {outdir / 'analyst_explanations.csv'}")
    print(f"Saved prompts to {outdir / 'llm_prompts_for_review.csv'}")


if __name__ == "__main__":
    main()
