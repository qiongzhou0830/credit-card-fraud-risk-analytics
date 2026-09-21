# Credit Card Fraud Risk Analytics & ML Scoring Dashboard

This project analyzes transaction-level credit card fraud data and builds a machine learning risk-scoring workflow for fraud monitoring and threshold-based review decisions.

## Project Goals

- Analyze fraud patterns across transaction amount and relative time buckets.
- Build baseline machine learning models for fraud risk scoring.
- Evaluate model performance under severe class imbalance using precision, recall, F1-score, ROC-AUC, and average precision (AP).
- Compare fraud-score thresholds to understand false positives, missed fraud, and manual-review workload.
- Use a simple cost analysis to illustrate threshold tradeoffs.
- Build a Tableau dashboard to communicate model and threshold results.
- Use SHAP to identify local model signals for selected high-risk transactions.
- Use an LLM to turn verified model evidence into short analyst-facing notes, then run simple rule-based faithfulness checks.

## Overview

The project uses the Kaggle Credit Card Fraud Detection dataset with 284,807 transactions, including 492 fraud cases. Because the target is highly imbalanced, accuracy alone is not useful enough for model comparison. The analysis focuses primarily on precision, recall, F1-score, and average precision.

Two models are compared:

- Logistic Regression with class balancing as a baseline.
- Random Forest with class balancing as the stronger model used for downstream threshold analysis.

In the current experiment, Random Forest achieved precision 0.648, recall 0.847, F1 0.735, and average precision 0.800 at the default 0.50 threshold. Logistic Regression achieved higher recall but much lower precision.

## Threshold and Cost Analysis

Random Forest probability scores are evaluated at thresholds from 0.05 to 0.90. Lower thresholds catch more fraud but create more false positives and manual-review workload; higher thresholds reduce workload but miss more fraud.

The simple cost example assigns a $5 cost to each false-positive investigation and adds the dollar amount of missed fraudulent transactions. Under this illustrative assumption, threshold 0.30 has the lowest estimated cost among the tested thresholds.

This threshold analysis is exploratory and is performed on the held-out test split used in the notebook. In a production modeling workflow, threshold selection should be performed on a separate validation set and final performance should be reported on an untouched test set.

## Dashboard

Tableau Public dashboard:

[View Tableau Dashboard](https://public.tableau.com/app/profile/qiong.zhou/viz/CreditCardFraudAnalysis_17818274072020/FraudRiskDashboard)

The dashboard was built from the original analytics and model outputs and shows model comparison, precision/recall tradeoffs, review workload, and the simple threshold cost analysis.

## SHAP + LLM Explanation Layer

The final explanation workflow is implemented in [`notebooks/04_llm_explanation_layer.ipynb`](notebooks/04_llm_explanation_layer.ipynb).

The Random Forest remains the fraud model; the LLM does not predict fraud. At threshold 0.30, 271 test-set transactions are sent to review. The notebook selects the 50 highest-scoring review transactions for explanation, then uses SHAP to identify the three strongest positive local contributions for each selected transaction.

For API-cost control, the notebook sends the first 10 prepared explanation records to an OpenAI model. The prompt includes only verified evidence: transaction ID, amount, fraud score, threshold, review decision, and the three SHAP signals. The dataset features are anonymized (`V1`-`V28`), so the prompt explicitly prevents the model from inventing merchant, cardholder, device, identity, location, or other unsupported real-world details.

A final rule-based check verifies that each generated note contains the fraud score, review threshold, and local feature names, and flags unsupported real-world terms. The saved run produced 10 LLM explanations and all 10 passed these basic checks. These checks are intentionally limited and do not replace human review.

```text
Random Forest score
-> threshold decision
-> top 50 high-risk review records
-> local SHAP signals
-> 10 LLM analyst notes
-> basic faithfulness checks
```

See [`reports/llm_explanations/README.md`](reports/llm_explanations/README.md) for the saved outputs from this workflow.

## Data

The original dataset is not committed because of its size. Download Kaggle's Credit Card Fraud Detection `creditcard.csv` and place it at:

```text
data/raw/creditcard.csv
```

`Time` in this dataset is elapsed seconds from the first recorded transaction, not a true clock-of-day timestamp. The EDA notebook therefore uses the derived 0-23 value only as a relative 24-hour time bucket, not as a verified local hour of day.

The explanation notebook requires `shap`, `openai`, and an OpenAI API key provided through the `OPENAI_API_KEY` environment variable. No API key is stored in this repository.
