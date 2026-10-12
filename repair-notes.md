# Repair notes

Fill this in during the timed assessment. Record what the cluster showed. Do not invent extra faults. No paid tools were used.

## Task 1 — Startup

- Original diagnostic (quote the status, describe line, or event that names the startup problem):
- Root cause:
- File and change:
- Verification command and result (`APP_ENV` must be `local`; pod may still be unready):

## Task 2 — Readiness

- Original diagnostic (quote the readiness failure):
- Root cause:
- File and change (readiness check kept):
- Verification command and result (rollout finished, current pod `1/1` Running):
- Readiness explanation (one sentence: how a readiness failure affects Service traffic, and how that differs from a liveness failure):

## Task 3 — Service access

- Original diagnostic (Service, pod labels, and endpoint or EndpointSlice evidence):
- Root cause:
- File and change (Service name, ports, and workload identity kept):
- Verification command and result (ready backend, then HTTP status and body from `http://cloudnotes/health`):
- Traffic flow explanation (how the Service selects pods, how a ready endpoint is chosen, and how the in-cluster request reaches the app):
