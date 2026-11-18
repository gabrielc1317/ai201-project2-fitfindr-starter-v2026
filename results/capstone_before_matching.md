# FitFindr capstone before: matching

- Hosted endpoint: https://fit-findr.onrender.com/ask
- Completed HTTP requests: 30 of 30
- Method: sequential HTTP requests from the client; wall-clock durations include network transit
- Limitation: this is an HTTP/API proxy, not an automated browser DOM check
- Limitation: Render's structured server logs and Gemini token counts require independent verification

| Trial | HTTP proxy passes | Time <= 30s | Criterion outcome |
|---|---:|---:|---|
| 1 | 2/10 | 2/10 | MISS / INCOMPLETE |
| 2 | 0/10 | 0/10 | MISS / INCOMPLETE |
| 3 | 0/10 | 0/10 | MISS / INCOMPLETE |

For Unit 9 C1: require 10/10 completed outputs per trial and verify actual browser rendering.
For Unit 9 C5: target >= 9/10 <=30s per trial based on browser-visible latency; HTTP duration here is a proxy.

## Failures to diagnose

- Trial 1 M03: HTTP 502, 14834.61ms, incomplete or failed workflow; error=None
- Trial 1 M04: HTTP 502, 117.23ms, incomplete or failed workflow; error=None
- Trial 1 M05: HTTP 502, 295.16ms, incomplete or failed workflow; error=None
- Trial 1 M06: HTTP 502, 146.22ms, incomplete or failed workflow; error=None
- Trial 1 M07: HTTP 502, 150.04ms, incomplete or failed workflow; error=None
- Trial 1 M08: HTTP 502, 163.32ms, incomplete or failed workflow; error=None
- Trial 1 M09: HTTP 502, 290.83ms, incomplete or failed workflow; error=None
- Trial 1 M10: HTTP 502, 133.54ms, incomplete or failed workflow; error=None
- Trial 2 M01: HTTP 502, 159.17ms, incomplete or failed workflow; error=None
- Trial 2 M02: HTTP 502, 177.74ms, incomplete or failed workflow; error=None
- Trial 2 M03: HTTP 502, 147.13ms, incomplete or failed workflow; error=None
- Trial 2 M04: HTTP 502, 340.4ms, incomplete or failed workflow; error=None
- Trial 2 M05: HTTP 502, 153.44ms, incomplete or failed workflow; error=None
- Trial 2 M06: HTTP 502, 161.65ms, incomplete or failed workflow; error=None
- Trial 2 M07: HTTP 502, 266.27ms, incomplete or failed workflow; error=None
- Trial 2 M08: HTTP 502, 157.04ms, incomplete or failed workflow; error=None
- Trial 2 M09: HTTP 502, 157.1ms, incomplete or failed workflow; error=None
- Trial 2 M10: HTTP 502, 143.01ms, incomplete or failed workflow; error=None
- Trial 3 M01: HTTP 502, 158.24ms, incomplete or failed workflow; error=None
- Trial 3 M02: HTTP 502, 153.33ms, incomplete or failed workflow; error=None
- Trial 3 M03: HTTP 502, 141.43ms, incomplete or failed workflow; error=None
- Trial 3 M04: HTTP 502, 130.58ms, incomplete or failed workflow; error=None
- Trial 3 M05: HTTP 502, 161.18ms, incomplete or failed workflow; error=None
- Trial 3 M06: HTTP 502, 150.88ms, incomplete or failed workflow; error=None
- Trial 3 M07: HTTP 502, 155.24ms, incomplete or failed workflow; error=None
- Trial 3 M08: HTTP 502, 157.04ms, incomplete or failed workflow; error=None
- Trial 3 M09: HTTP 502, 245.42ms, incomplete or failed workflow; error=None
- Trial 3 M10: HTTP 502, 144.82ms, incomplete or failed workflow; error=None
