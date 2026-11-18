# FitFindr capstone after2: matching

- Hosted endpoint: https://fit-findr.onrender.com/ask
- Completed HTTP requests: 30 of 30
- Method: sequential HTTP requests from the client; wall-clock durations include network transit
- Limitation: this is an HTTP/API proxy, not an automated browser DOM check
- Limitation: Render's structured server logs and Gemini token counts require independent verification

| Trial | HTTP proxy passes | Time <= 30s | Criterion outcome |
|---|---:|---:|---|
| 1 | 10/10 | 10/10 | PASS |
| 2 | 10/10 | 10/10 | PASS |
| 3 | 10/10 | 10/10 | PASS |

For Unit 9 C1: require 10/10 completed outputs per trial and verify actual browser rendering.
For Unit 9 C5: target >= 9/10 <=30s per trial based on browser-visible latency; HTTP duration here is a proxy.

## Failures to diagnose

- None for the HTTP proxy; browser/log evidence still required.
