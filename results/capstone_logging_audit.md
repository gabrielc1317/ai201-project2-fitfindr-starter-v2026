# FitFindr — after2 observability audit

**Source:** Render text log export, 2026-11-18 04:18:19–04:25:26 UTC. The 10 JSONL records are verbatim selected objects from the uploaded export, not synthetic test fixtures.

## Complete-log audit

- Total structured `/ask` JSON records: **60**
- Correct mandatory top-level fields (`timestamp`, `request_id`, `input`, `output`, `duration_ms`, `queue_ms`, `stages_ms`): **60/60**
- Unique request IDs: **60/60**
- Complete successful responses (HTTP 200, selected item, no error): **30**; all four stages appear
- No-result responses (HTTP 200, no selected item, user guidance): **15**; only `parse` and `mcp_search` appear
- Rejected invalid responses (HTTP 400, explanatory error): **15**; `stages_ms` is empty
- HTTP 500/502 responses in this exported after2 test window: **0**
- C4 target 10/10 complete logs: **MET** (60/60 in observed test window).

### Ten representative records

| Path | Request ID | HTTP | Server duration (ms) |
|---|---|---:|---:|
| invalid | `05bf64fa12a24612b6d26d2bbf9d3bf1` | 400 | 0.40 |
| invalid | `c14c6889b49c463da065ad9d2fa4af17` | 400 | 0.20 |
| invalid | `2673172f6de24e34ba5968b8177ff9b0` | 400 | 0.22 |
| no match | `0b478c184d6b4464b6d20fb98578a516` | 200 | 10028.24 |
| no match | `ee805f3d7da44715bc90fbb691ebc17a` | 200 | 4082.55 |
| no match | `86083b18ec8d4bb6b2eb57e92ca04909` | 200 | 4285.66 |
| completed | `c702b4690bec499dbe2c9e24129e6713` | 200 | 23154.10 |
| completed | `1770edffc1f346dfb22312a41b724739` | 200 | 21751.21 |
| completed | `3adf98d9291e44f380dce04765673757` | 200 | 8426.85 |
| completed | `42c63870eec9420db9521e7ef75b7a02` | 200 | 8683.04 |

All ten raw JSON objects are stored in `capstone_log_samples.jsonl`; copy into the repo's `results/` folder.

## Limits and notes

- The exported records verify structured server-side logs, **not** browser rendering or user-perceived latency.
- A logged success/failure flag describes agent execution, not whether a Render health check or gateway operation could have failed before Flask received the request.
- For invalid non-string query values, current `observability.py` normalizes `input.query` to the empty string, so the raw malformed type is not available in the log; the response and HTTP status remain correct.
- `stages_ms` provides stage duration breakdown, not Gemini token usage or billed monetary cost. In particular, a subprocess owns the `suggest_outfit` Gemini calls, so parent-process token counters omit those calls.
- HTTP 200 with `output.success=false` is valid for the expected no-match business outcome; this is not a 5xx server failure.
- Server `queue_ms` is zero in these sequential trials and is not a reliable estimate of ingress waiting at a proxy.

## Measured latency from successful requests

For the first ten successful search+outfit+card requests, mean server duration is **17.989 seconds**. Total of these ten server durations is **179.889 seconds**. These are wall-clock server durations and should not be called paid CPU seconds or billed Gemini compute.

For all 30 successful runs, mean server duration is **11.635 seconds**. Trial 2/3 caching lowered repeated-response durations, so raw averages should be reported with cache status.
