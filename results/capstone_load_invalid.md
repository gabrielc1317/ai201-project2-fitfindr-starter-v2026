# FitFindr — 1× versus 10× arrival-rate observation

- Scenario: `invalid`; requests per phase: 20; client maximum in flight: 2.
- 1× offered rate: 0.500 requests/s (every 2.00s).
- 10× offered rate: 5.000 requests/s (every 0.20s).
- All requests target the hosted Render `/ask`; a background client probes `/health` once per interval.
- Zero Gemini calls expected: invalid bodies are rejected before agent execution; impossible zero-result searches stop before outfit generation.
- This is an offered-rate experiment; dispatch backlog in the client executor reduces actual HTTP send rate under saturation.
- Health probes, application logs, and client HTTP timing measure different layers; server `queue_ms` cannot measure reverse proxy waits.

| Metric | 1× | 10× |
|---|---:|---:|
| Offered requests/s | 0.5 | 5.0 |
| Achieved initial HTTP dispatches/s | 0.5 | 5.0 |
| Requests completed | 20 | 20 |
| Expected HTTP results | 20 | 20 |
| Unexpected responses | 0 | 0 |
| Mean client latency (ms) | 116.91 | 103.33 |
| p50 client latency (ms) | 108.86 | 102.21 |
| p95 client latency (ms) | 159.19 | 115.02 |
| Maximum client latency (ms) | 168.98 | 120.28 |
| Successful /health checks | 35 | 4 |
| Total /health checks | 35 | 4 |
| Peak client in-flight requests | 1 | 1 |
| Maximum client-dispatch delay (ms) | 0.71 | 0.47 |

## Interpretation limits

- Invalid-request scenario measures fast validation and HTTP responsiveness **only**. It does not represent full Gemini+MCP search throughput.
- Zero-result scenario executes MCP search without creating outfits, but it is not a full successful agent workload.
- A local thread-pool limit is a client-side safety mechanism, not a server concurrency result. Compare achieved dispatch rate with offered rate.
- If 10× is skipped due to health or 5xx failure, that is a valid observed limitation and should not be filled with invented values.
