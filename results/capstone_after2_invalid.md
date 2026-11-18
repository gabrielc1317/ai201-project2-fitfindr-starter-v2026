# FitFindr capstone after2: invalid

- Hosted endpoint: https://fit-findr.onrender.com/ask
- Completed HTTP requests: 15 of 15
- Method: sequential HTTP requests from the client; wall-clock durations include network transit
- Limitation: this is an HTTP/API proxy, not an automated browser DOM check
- Limitation: Render's structured server logs and Gemini token counts require independent verification

| Trial | HTTP proxy passes | Time <= 30s | Criterion outcome |
|---|---:|---:|---|
| 1 | 5/5 | 5/5 | PASS |
| 2 | 5/5 | 5/5 | PASS |
| 3 | 5/5 | 5/5 | PASS |

For Unit 9 C2: also confirm no MCP stages or Gemini calls ran in server logs.
Browser may reject empty text before sending a request; test that UI behavior separately.

## Failures to diagnose

- None for the HTTP proxy; browser/log evidence still required.
