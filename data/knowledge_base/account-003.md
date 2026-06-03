# Two-Factor Authentication (2FA) Issues

This guide covers common 2FA problems and how to help customers regain access when 2FA is blocking them.

## TOTP code not accepted

- Ensure the customer's device clock is correctly synced (TOTP codes are time-based, a clock drift of >30s causes failure).
- Ask the customer to regenerate the code from their authenticator app and try again immediately.
- If the device time is correct, the customer may be using the wrong account's TOTP entry.

## Lost authenticator app

If the customer no longer has access to their authenticator app:
1. Ask the customer to use one of their saved backup codes (provided at 2FA setup).
2. If backup codes are also lost, escalate to account recovery — requires identity verification.
3. After verification, disable 2FA on the account from the admin panel and instruct the customer to re-enroll.

## SMS 2FA not arriving

- Confirm the phone number on file is correct.
- Ask the customer to check they have signal and no call-blocking apps.
- Wait up to 5 minutes — SMS delivery can be delayed.
- If SMS fails repeatedly, offer to switch the customer to TOTP-based 2FA instead.

## Disabling 2FA

Support cannot disable 2FA without identity verification. This is a security control, not a policy preference.

KEYWORDS: two factor, 2fa, authenticator, totp, otp, backup codes, sms code, verification code, one time password, lost authenticator, mfa
