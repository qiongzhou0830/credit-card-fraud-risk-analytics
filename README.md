# Credit Card Fraud Risk Analytics & ML Scoring Dashboard

This project analyzes transaction-level credit card fraud data and builds a machine learning risk scoring pipeline to support fraud monitoring and threshold-based decision making.

## Project Goals

- Analyze fraud patterns across transaction amount and time.
- Build baseline machine learning models for fraud risk scoring.
- Evaluate model performance under class imbalance using precision, recall, F1-score, ROC-AUC, and PR-AUC.
- Compare decision thresholds to understand fraud detection tradeoffs, false positives, and investigation workload.
- Build a dashboard to communicate fraud risk metrics and model performance.
- Create short analyst-facing explanations for high-risk transactions and check whether the explanations stay close to the model output.

# Credit Card Fraud Risk Analytics

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

## Analyst Explanation Layer

I also added a small explanation layer for the fraud score results. The idea is that a fraud score by itself is not always easy to use. If a transaction is sent to manual review, an analyst should be able to see a short note explaining why it was flagged.

This part uses the model score, selected threshold, transaction amount, and anonymized feature signals to create simple review explanations. Since the dataset is anonymized, the explanations do not make claims about the merchant, cardholder identity, location, or transaction history.

I also added a basic check to flag explanations that may include unsupported details or miss important context. This is not a production system, but it helped me think about how model outputs can be made more useful and easier to review.


## Data

The original data comes from the Kaggle Credit Card Fraud Detection dataset.

I did not upload the full raw dataset because the file is too large for GitHub. To run the notebooks, download `creditcard.csv` from Kaggle and put it here:

```text
data/raw/creditcard.csv



