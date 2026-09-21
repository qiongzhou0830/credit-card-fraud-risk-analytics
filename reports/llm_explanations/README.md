# SHAP + LLM Explanation Outputs

This folder contains saved outputs from `notebooks/04_llm_explanation_layer.ipynb`.

## Output files

- `final_test_metrics.csv` — final metrics on the untouched test split after model and threshold selection were completed on validation data.
- `threshold_policy_table.csv` — validation precision, recall, F1, confusion counts, review workload, review rate, and illustrative cost across seven candidate thresholds.
- `precision_recall_by_threshold.png` — validation precision and recall across tested thresholds.
- `review_workload_by_threshold.png` — validation manual-review workload across tested thresholds.
- `flagged_transactions.csv` — the 50 highest-scoring test records classified as `Review` at the validation-selected threshold.
- `flagged_transaction_explanations_input.csv` — compact explanation inputs containing record ID, amount, fraud score, review decision, selected threshold, and three strongest positive local SHAP contributions.
- `analyst_explanations.csv` — 10 analyst-facing notes generated from verified explanation inputs.
- `llm_explanation_faithfulness_review.csv` — basic rule-based checks for the generated notes.
- `project_summary.txt` — concise summary of the saved notebook run.

## Saved run

- Selected model: Random Forest
- Validation-selected threshold: 0.50
- Final test Average Precision (AP): 0.793
- Final test PR-AUC (trapezoidal): 0.795
- Final test precision: 0.820
- Final test recall: 0.837
- Test records sent to review: 100
- Highest-scoring review records prepared for SHAP explanation: 50
- LLM notes generated: 10
- Notes passing the basic checks: 10/10

## Important limitations

The Kaggle features `V1`-`V28` are anonymized. SHAP values describe local model contributions, but they do not reveal real-world meanings such as merchant identity, device, cardholder identity, or location.

The rule-based faithfulness check is intentionally narrow. Passing it means the generated note contains the expected score, threshold, and feature names and avoids a small list of unsupported terms; it is not a guarantee of full factual correctness or production safety.

The model and review threshold are selected using validation data. The final metrics above are reported on an untouched test split.
