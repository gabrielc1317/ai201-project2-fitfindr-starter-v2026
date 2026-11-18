# FitFindr capstone before: invalid

- Hosted endpoint: https://fit-findr.onrender.com/ask
- Completed HTTP requests: 15 of 15
- Method: sequential HTTP requests from the client; wall-clock durations include network transit
- Limitation: this is an HTTP/API proxy, not an automated browser DOM check
- Limitation: Render's structured server logs and Gemini token counts require independent verification

| Trial | HTTP proxy passes | Time <= 30s | Criterion outcome |
|---|---:|---:|---|
| 1 | 3/5 | 3/5 | MISS / INCOMPLETE |
| 2 | 3/5 | 3/5 | MISS / INCOMPLETE |
| 3 | 3/5 | 3/5 | MISS / INCOMPLETE |

For Unit 9 C2: also confirm no MCP stages or Gemini calls ran in server logs.
Browser may reject empty text before sending a request; test that UI behavior separately.

## Failures to diagnose

- Trial 1 I04: HTTP 500, 168.24ms, invalid body not rejected with HTTP 400; error=None
- Trial 1 I05: HTTP 500, 148.46ms, invalid body not rejected with HTTP 400; error=None
- Trial 2 I04: HTTP 500, 126.41ms, invalid body not rejected with HTTP 400; error=None
- Trial 2 I05: HTTP 500, 128.39ms, invalid body not rejected with HTTP 400; error=None
- Trial 3 I04: HTTP 500, 109.78ms, invalid body not rejected with HTTP 400; error=None
- Trial 3 I05: HTTP 500, 105.44ms, invalid body not rejected with HTTP 400; error=None
