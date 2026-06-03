# Payment Failure and Retry Policy

When a payment fails, the system automatically retries before suspending the account. This document describes the retry schedule and how to help customers with failed payments.

## Automatic retry schedule

- Day 0: Initial charge fails → customer notified by email
- Day 3: First retry
- Day 7: Second retry
- Day 14: Final retry → account suspended if still unpaid

## Common causes of payment failure

- Expired credit card
- Insufficient funds
- Card issuer blocking international transaction
- Incorrect billing address (AVS mismatch)
- 3D Secure authentication not completed

## Resolving a failed payment

1. Ask the customer to update their payment method in account settings.
2. Once updated, trigger a manual retry from the billing dashboard.
3. If the customer has a valid card but payments keep failing, advise them to contact their bank.

## Account reinstatement

After a successful payment following suspension, the account is reinstated automatically within 15 minutes. Data is not lost during the suspension period.

KEYWORDS: payment failed, payment failure, card declined, charge failed, billing failed, retry payment, suspended account, expired card, insufficient funds
