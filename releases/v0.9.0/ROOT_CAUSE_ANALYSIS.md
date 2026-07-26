# Root Cause Analysis Reference - v0.9.0

The Root Cause Engine correlates findings across all scanners and infers probable causes.

## Confidence Calculation
- Base confidence: 50%
- +5% per finding in group
- +20% if group contains CRITICAL or ERROR severity
- Capped at 99%
