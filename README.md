# Credit Card Fraud Risk Analytics & ML Scoring Dashboard

This project analyzes transaction-level credit card fraud data and builds a machine learning risk scoring pipeline to support fraud monitoring and threshold-based decision making.

## Project Goals

- Analyze fraud patterns across transaction amount and time.
- Build baseline machine learning models for fraud risk scoring.
- Evaluate model performance under class imbalance using precision, recall, F1-score, ROC-AUC, and PR-AUC.
- Compare decision thresholds to understand fraud detection tradeoffs, false positives, and investigation workload.
- Build a dashboard to communicate fraud risk metrics and model performance.
- Use SHAP to find the local model signals behind individual high-risk transactions.
- Use an LLM to turn verified model evidence into short analyst-facing notes, then run basic faithfulness checks.

## Overview

This is a small data analytics and machine learning project about credit card fraud detection. I used the Kaggle Credit Card Fraud Detection dataset to practice EDA, model evaluation, threshold analysis, and Tableau dashboarding.

The dataset is highly imbalanced, so I did not only look at accuracy. I focused more on precision, recall, PR-AUC, and how different fraud score thresholds change the number of false positives and missed fraud cases.

## Dashboard

I made a Tableau dashboard for this project:

[View Tableau Dashboard](https://public.tableau.com/app/profile/qiong.zhou/viz/CreditCardFraudAnalysis_17818274072020/FraudRiskDashboard)

The dashboard shows:

- model comparison between Logistic Regression and Random Forest
- precision and recall at different thresholds
- review workload at different thresholds
- a simple cost analysis for false positives and missed fraud
- fraud score explanations and review notes for high-risk transactions

## SHAP and LLM Explanation Layer

The full explanation workflow is in [`notebooks/04_llm_explanation_layer.ipynb`](notebooks/04_llm_explanation_layer.ipynb).

The Random Forest still makes the fraud prediction. For each transaction sent to review, SHAP finds the three local features that pushed its fraud score higher. The notebook then sends only the verified score, threshold, amount, and SHAP signals to an OpenAI model, which writes a short note for a fraud analyst.

The dataset contains anonymized features such as `V1` to `V28`, so the prompt tells the model not to invent a merchant, cardholder, device, identity, or location. A final rule-based check confirms that the score, threshold, and local feature names appear in the explanation and flags unsupported real-world terms. These checks are intentionally simple and do not replace human review.

The pipeline is:

```text
Random Forest score -> threshold decision -> local SHAP signals -> LLM note -> faithfulness checks
```

## Data

The original data comes from the Kaggle Credit Card Fraud Detection dataset.

I did not upload the full raw dataset because the file is too large for GitHub. To run the notebooks, download `creditcard.csv` from Kaggle and put it here:

```text
data/raw/creditcard.csv
```

The explanation notebook also requires `shap`, `openai`, and an OpenAI API key stored in the `OPENAI_API_KEY` environment variable. It generates only 10 LLM explanations by default to limit API usage.
