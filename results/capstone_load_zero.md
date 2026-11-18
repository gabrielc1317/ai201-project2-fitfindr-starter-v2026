# FitFindr — 1× versus 10× arrival-rate observation

- Scenario: `zero`; requests per phase: 6; client maximum in flight: 2.
- 1× offered rate: 0.100 requests/s (every 10.00s).
- 10× offered rate: 1.000 requests/s (every 1.00s).
- All requests target the hosted Render `/ask`; a background client probes `/health` once per interval.
- Zero Gemini calls expected: invalid bodies are rejected before agent execution; impossible zero-result searches stop before outfit generation.
- This is an offered-rate experiment; dispatch backlog in the client executor reduces actual HTTP send rate under saturation.
- Health probes, application logs, and client HTTP timing measure different layers; server `queue_ms` cannot measure reverse proxy waits.

| Metric | 1× | 10× |
|---|---:|---:|
| Offered requests/s | 0.1 | 1.0 |
| Achieved initial HTTP dispatches/s | 0.1 | 0.287 |
| Requests completed | 6 | 6 |
| Expected HTTP results | 6 | 6 |
| Unexpected responses | 0 | 0 |
| Mean client latency (ms) | 5462.44 | 7764.31 |
| p50 client latency (ms) | 4509.68 | 8497.37 |
| p95 client latency (ms) | 9115.51 | 8904.1 |
| Maximum client latency (ms) | 10465.85 | 8904.76 |
| Successful /health checks | 49 | 24 |
| Total /health checks | 49 | 24 |
| Peak client in-flight requests | 2 | 2 |
| Maximum client-dispatch delay (ms) | 0.51 | 12394.29 |

## Interpretation limits

- Invalid-request scenario measures fast validation and HTTP responsiveness **only**. It does not represent full Gemini+MCP search throughput.
- Zero-result scenario executes MCP search without creating outfits, but it is not a full successful agent workload.
- A local thread-pool limit is a client-side safety mechanism, not a server concurrency result. Compare achieved dispatch rate with offered rate.
- If 10× is skipped due to health or 5xx failure, that is a valid observed limitation and should not be filled with invented values.
