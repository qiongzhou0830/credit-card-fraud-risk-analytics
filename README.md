# Credit Card Fraud Risk Analytics & ML Scoring Dashboard

This project analyzes transaction-level credit card fraud data and builds a machine-learning risk-scoring workflow for fraud monitoring, threshold-based review decisions, and analyst-facing explanations.

## Project Goals

- Analyze fraud patterns across transaction amount and relative time buckets.
- Train fraud-risk models under severe class imbalance.
- Separate model training, model selection, threshold tuning, and final testing.
- Evaluate performance using precision, recall, F1-score, Average Precision (AP), PR-AUC, and reference ROC-AUC.
- Compare fraud-score thresholds by review workload, missed fraud, and an illustrative business-cost assumption.
- Use SHAP to identify local model signals for selected high-risk records.
- Use an LLM to turn verified model evidence into short analyst-facing notes, then run simple rule-based faithfulness checks.
- Communicate model and threshold tradeoffs through Tableau.

## Data

The project uses the Kaggle Credit Card Fraud Detection dataset with 284,807 transactions, including 492 fraud cases.

The original dataset is not committed because of its size. Download `creditcard.csv` and place it at:

```text
data/raw/creditcard.csv
```

`Time` is elapsed seconds from the first recorded transaction, not a true clock-of-day timestamp. The EDA notebook therefore uses the derived 0-23 value only as a relative 24-hour time bucket.

## Modeling Workflow

The modeling workflow uses a stratified 60/20/20 train/validation/test split:

```text
training set
-> validation model selection
-> validation threshold selection
-> untouched test evaluation
```

Logistic Regression and Random Forest are trained on the training split. Average Precision (AP) is the primary model-selection metric on validation data because the target is highly imbalanced. PR-AUC is reported separately using trapezoidal integration rather than being used interchangeably with AP.

Validation results:

- Logistic Regression: AP 0.683, precision 0.059, recall 0.899 at threshold 0.50.
- Random Forest: AP 0.748, precision 0.835, recall 0.768 at threshold 0.50.

Random Forest is therefore selected for downstream scoring.

## Threshold and Cost Analysis

Seven candidate thresholds from 0.05 to 0.90 are compared on the validation split.

The illustrative cost model assigns:

- $5 to each false-positive investigation.
- the transaction amount to each missed fraudulent transaction.

Under this assumption, threshold **0.50** has the lowest estimated validation cost among the tested thresholds.

After the model and threshold are fixed, they are evaluated once on the untouched test split.

Final test results:

- Precision: **0.820**
- Recall: **0.837**
- F1-score: **0.828**
- Average Precision (AP): **0.793**
- PR-AUC (trapezoidal): **0.795**
- ROC-AUC (reference): **0.978**

## SHAP + LLM Explanation Layer

The final explanation workflow is implemented in [`notebooks/04_llm_explanation_layer.ipynb`](notebooks/04_llm_explanation_layer.ipynb).

The Random Forest remains the fraud model; the LLM does not predict fraud.

At the validation-selected threshold of 0.50:

- 100 test records are sent to manual review.
- the 50 highest-scoring review records are prepared for local SHAP explanation.
- the first 10 prepared records are sent to the OpenAI API for analyst-facing notes.
- all 10 generated notes pass the project's basic rule-based checks.

The LLM receives only verified evidence: record ID, transaction amount, fraud score, review threshold, and the three strongest positive local SHAP contributions.

Because `V1`-`V28` are anonymized, the prompt explicitly prevents unsupported claims about merchant, cardholder, device, identity, IP address, location, or other real-world meanings.

```text
Random Forest score
-> validation-selected threshold
-> test-set review decision
-> top 50 high-risk review records
-> local SHAP signals
-> 10 LLM analyst notes
-> basic faithfulness checks
```

See [`reports/llm_explanations/README.md`](reports/llm_explanations/README.md) for the saved outputs.

## OpenAI API Key

The notebook prompts the user to enter an OpenAI API key at runtime using `getpass`, so the key is hidden while typing and is not saved in notebook output.

Do not commit a real API key to a public repository.

## Dashboard

Tableau Public dashboard:

[View Tableau Dashboard](https://public.tableau.com/app/profile/qiong.zhou/viz/CreditCardFraudAnalysis_17818274072020/FraudRiskDashboard)

The dashboard was built from the original analytics/modeling stage and communicates fraud distribution, model performance, and threshold tradeoffs.
