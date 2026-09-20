# Prompt Used for Optional LLM Explanations

I used this prompt only to explain model output in plain English.  
The LLM is not used to predict fraud.

```text
Write a short explanation for a fraud analyst.

Use only the information below. Do not make up merchant, identity, location, device, or transaction history.

Transaction ID: {transaction_id}
Amount: {amount}
Fraud score: {fraud_score}
Threshold: {selected_threshold}
Decision: {review_decision}
Risk notes: {risk_notes}
Threshold note: {threshold_note}

Write 2 short sentences.
```

After generating explanations, I check whether the explanation invented anything that was not in the model output.
