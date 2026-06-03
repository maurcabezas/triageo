# Data Retention and Deletion Schedules

This document describes how long different types of data are retained and when they are automatically deleted.

## Retention schedule

| Data type | Retention period | Notes |
|---|---|---|
| Active account data | Indefinitely | While account is active |
| Cancelled account data | 90 days | Then deleted unless legal hold |
| Billing records | 7 years | Tax and legal compliance |
| Activity logs | 12 months | Rolling window |
| Support ticket records | 3 years | Audit purposes |
| Deleted content | 30 days | Recovery window, then purged |
| Backups | 30 days | Rolling backup retention |

## Legal hold

Data under a legal hold is exempt from automated deletion. Legal holds must be applied and removed by the legal team only.

## Customer-initiated deletion

When a customer requests data deletion (GDPR Article 17), the account is marked for deletion and the automated schedule above is accelerated to 30 days from request confirmation.

## Data residency

By default all data is stored in the EU region. Enterprise customers can request US or APAC region storage at contract time.

KEYWORDS: data retention, deletion schedule, data deletion, retention policy, backup retention, legal hold, data residency, gdpr retention, account deletion timeline
