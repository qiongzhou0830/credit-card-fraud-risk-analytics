# SHAP + LLM Explanation Outputs

This folder contains outputs from `notebooks/04_llm_explanation_layer.ipynb`.

Notebook 04 is downstream of the modeling pipeline in `notebooks/02_ml_risk_scoring.ipynb`. Model selection and threshold selection are completed in Notebook 02; Notebook 04 reuses those fixed choices and focuses only on explaining records sent to manual review.

## Output files

- `flagged_transactions.csv` — the 50 highest-scoring test records sent to `Review` by the fixed Random Forest policy at the validation-selected threshold.
- `flagged_transaction_explanations_input.csv` — compact explanation inputs with record ID, amount, fraud score, selected threshold, review decision, and the three strongest positive local SHAP contributions.
- `analyst_explanations.csv` — 10 analyst-facing notes generated from the verified explanation inputs.
- `llm_explanation_faithfulness_review.csv` — basic rule-based checks confirming that the generated notes include the expected score, threshold, and local feature names while avoiding a small set of unsupported real-world claims.
- `project_summary.txt` — concise summary of the saved explanation-layer run.

## Saved run

- Selected model from Notebook 02: Random Forest
- Validation-selected threshold: 0.50
- Test records sent to review: 100
- Highest-scoring review records prepared for SHAP explanation: 50
- LLM notes generated: 10
- Notes passing the basic checks: 10/10

## Workflow

`fixed risk policy -> Review records -> local SHAP signals -> constrained LLM analyst notes -> basic faithfulness checks`

## Important limitations

The Kaggle features `V1`-`V28` are anonymized. SHAP values describe local model contributions, but they do not reveal real-world meanings such as merchant identity, device, cardholder identity, or location.

The LLM does not make the fraud decision. It only converts verified model outputs and SHAP signals into a short analyst-facing note.

The rule-based faithfulness check is intentionally narrow. Passing it means the note contains the expected evidence and avoids a small list of unsupported terms; it is not a guarantee of full factual correctness or production safety.

Final model-selection, threshold-selection, and untouched-test evaluation outputs belong to Notebook 02 and are stored under `data/processed/`, rather than duplicated in this explanation-output folder.
