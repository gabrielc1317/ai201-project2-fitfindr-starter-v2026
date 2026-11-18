# FitFindr Unit 9 — Ten-run measured cost and capacity analysis

## Provenance and method
- Source: actual Render structured `/ask` records in `Pasted text(20261118-043108).txt`.
- Sample: first 10 complete successful HTTP 200 search → MCP outfit → fit card requests in supplied export.
- Measurements: server wall-clock and application stage timings; **not** paid CPU seconds or provider billing records.
- Model: `gemini-3.5-flash-lite` configured in `config.py` unless deployment environment overrides `AI201_MODEL`.
- Model-output caching may affect calls and latency. These ten are the first matching trial after deployment; do not extrapolate later cache-accelerated trials as independent uncached calls.

## Observed ten-run timings

| Metric | Measured value |
|---|---:|
| Successful requests | 10/10 |
| Total server wall time | 179.889 s |
| Mean server wall time / request | 17.989 s |
| Median server wall time / request | 16.829 s |
| Minimum / maximum server time | 16.055 / 23.154 s |
| Mean `parse` | 0.0000 s |
| Mean `mcp_search` | 4.1948 s |
| Mean `mcp_outfit` | 12.2037 s |
| Mean `fit_card` | 1.5896 s |

### Evidence per request

| Run | UTC timestamp | Request ID | Server time (s) |
|---:|---|---|---:|
| 1 | 2026-11-18T04:19:56.334023+00:00 | `c702b4690bec…` | 23.154 |
| 2 | 2026-11-18T04:20:12.832370+00:00 | `5a38187fc3b2…` | 16.332 |
| 3 | 2026-11-18T04:20:31.458745+00:00 | `91427b2f85e1…` | 18.498 |
| 4 | 2026-11-18T04:20:49.159888+00:00 | `744b23e41eb8…` | 17.560 |
| 5 | 2026-11-18T04:21:05.347817+00:00 | `c8e9c418d1d1…` | 16.055 |
| 6 | 2026-11-18T04:21:22.344922+00:00 | `0aeba0236ffa…` | 16.887 |
| 7 | 2026-11-18T04:21:39.134492+00:00 | `405c1c81d865…` | 16.606 |
| 8 | 2026-11-18T04:21:55.577893+00:00 | `83f1fa317636…` | 16.274 |
| 9 | 2026-11-18T04:22:12.514840+00:00 | `62e8492836b5…` | 16.771 |
| 10 | 2026-11-18T04:22:34.375924+00:00 | `1770edffc1f3…` | 21.751 |

Complete per-request fields and stage times: [`capstone_cost_10run.csv`](capstone_cost_10run.csv).

## Provider usage and monetary cost

Google Gemini Developer API Standard paid-tier prices (USD per 1 million tokens) for `gemini-3.5-flash-lite`:
- Input: $0.30; output (including thinking tokens): $2.50.
- Gemini Free Tier is listed as free of charge for eligible usage but has rate/quota constraints. Actual bill depends on the account/tier and uncached calls.
- Official source (checked 2026-11-17): https://ai.google.dev/gemini-api/docs/pricing.md

The application performs a Gemini request for `suggest_outfit` in a separate MCP subprocess and another for `create_fit_card` in the parent process. **Neither caller’s provider token counts were captured in this exported request log.** Parent-only token counts would understate usage. Model calls per successful uncached run are expected to be 2, so approximately 20 calls across these ten runs, but cache/retries can change the actual count.

| Metric | Actual result |
|---|---|
| Gemini input tokens (both processes) | Not measured |
| Gemini output tokens (both processes) | Not measured |
| Provider-billed API charge | Not measurable from these logs |

Do not convert wall time into model cost. If verified usage totals are later captured across **both** processes, rerun this script with `--measured-input-tokens` and `--measured-output-tokens` after moving existing output files aside (preserve originals).

## Scenario: 100 users per day

Assumptions: one full successful outfit request per user, similar input/wardrobe mix, no overlapping agent executions, and no model failures. This is a scenario, not an observed daily traffic forecast.

- Requests/day: `100 users/day × 1 request/user = 100 requests/day`.
- Uncached model calls/day: `100 requests × 2 calls = 200 calls/day` (excludes retries; actual may be lower with application-level cache).
- Cumulative serialized server wall time: `100 × 17.989 s = 29.98 minutes/day`.
- Average arrival if evenly distributed: `100 / 86,400 = 0.00116 requests/s` (about 4.17 requests/hour); bursts can queue.
- API charge projection for a **paid standard tier**, once per-request token totals are verified: `100 × (mean_input_tokens × $0.30 + mean_output_tokens × $2.50)/1,000,000` per day.

- Numerical API-dollar projection: **unavailable**, because full Gemini token usage was not logged. A free-tier cash charge cannot be inferred from elapsed time.

## Caveats

- `mcp_outfit` dominates measured latency, but its duration includes subprocess work and waiting for Gemini; it is not CPU utilization.
- `queue_ms` near zero in these sequential measurements says nothing about ingress queuing under burst load.
- Time spent asleep on Render and external service availability are not represented by ten warm successful requests.
- Gemini output billed usage may include thinking tokens; `candidates_token_count` alone may not capture them. Prefer provider usage metadata with thinking tokens accounted for.
