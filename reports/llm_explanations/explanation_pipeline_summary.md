# Fraud Score Explanation Layer

This is a small extension of my credit card fraud project.

The original project already had model scores, threshold analysis, and a Tableau dashboard. I added this part because a score by itself is hard to use. If a transaction is sent to manual review, an analyst should be able to see a short explanation of why it was flagged.

## What this part does

```text
scored transactions
→ choose threshold
→ select high-risk transactions
→ prepare explanation inputs
→ write short analyst explanations
→ check if the explanations made anything up
```

## Important limitation

The Kaggle fraud dataset has anonymized features like V1-V28. Because of that, I should not claim anything about the merchant, user identity, device, or location. The explanation should only talk about the model score, threshold, amount, and anonymized feature signals.

## Files created

- `explanation_input_sample.csv`
- `llm_prompts_for_review.csv`
- `analyst_explanations.csv`
- `faithfulness_review.csv`
- `faithfulness_review_summary.csv`

## How I would explain this in an interview

My fraud project originally focused on model performance and threshold tradeoffs. I added this explanation layer to make the model output easier for a human analyst to use. I also added a simple faithfulness check, because explanations can sound convincing even when they add details that were not actually in the data.
