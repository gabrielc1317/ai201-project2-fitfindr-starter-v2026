#!/usr/bin/env python3
"""FitFindr Unit 9 capstone HTTP baseline. Standard library only.

Use AFTER committing Unit 9 acceptance criteria and BEFORE implementing
measured improvements. This exercises POST /ask, not the visual DOM.

Examples:
  python capstone_baseline.py --group invalid --phase before
  python capstone_baseline.py --group zero --phase before
  python capstone_baseline.py --group matching --phase before
  python capstone_baseline.py --group matching --phase after1

The script runs sequentially to respect the single-worker MCP architecture.
It writes client-side HTTP evidence to results/. It does not verify Render's
server-side logs or the browser DOM; evaluate those separately.
"""

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MATCHING = [
    ("M01", "vintage graphic tee under $30"),
    ("M02", "90s track jacket size M"),
    ("M03", "vintage polo shirt under $25"),
    ("M04", "denim jacket under $50"),
    ("M05", "platform sneakers under $50"),
    ("M06", "brown leather belt under $15"),
    ("M07", "corduroy pants under $35"),
    ("M08", "flannel shirt under $25"),
    ("M09", "black mesh top under $20"),
    ("M10", "vintage band tee under $20"),
]

# Every zero case has a maximum below the dataset's minimum listing price ($12).
# These test a DEFINITE zero-result path; semantic-relevance probes can be
# added separately without confusing the initial acceptance verdict.
ZERO = [
    ("Z01", "designer ballgown size XXS under $5"),
    ("Z02", "silver cowboy boots under $2"),
    ("Z03", "antique kimono under $3"),
    ("Z04", "haute couture gown under $4"),
    ("Z05", "cashmere scarf under $1"),
]

INVALID = [
    ("I01", "Missing query", {}),
    ("I02", "Empty string", {"query": ""}),
    ("I03", "Whitespace only", {"query": "   "}),
    ("I04", "Number instead of string", {"query": 123}),
    ("I05", "Array instead of string", {"query": ["vintage tee"]}),
]

NO_MATCH = (
    "No listings matched your search. Try broadening the description, "
    "changing the size, or raising the maximum price."
)


def send(base, payload, timeout):
    req = Request(
        base.rstrip("/") + "/ask",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "FitFindr-Capstone-Eval/1.0"},
        method="POST",
    )
    status, raw, transport_error = None, b"", None
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as resp:
            status, raw = resp.status, resp.read()
    except HTTPError as exc:
        status, raw = exc.code, exc.read()
    except (URLError, TimeoutError, ConnectionError, OSError) as exc:
        transport_error = f"{type(exc).__name__}: {exc}"
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    try:
        data = json.loads(raw) if raw else None
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = None
    return status, data, elapsed, transport_error


def evaluate(group, status, data, elapsed, transport_error):
    d = data if isinstance(data, dict) else {}
    error = d.get("error")
    item = d.get("selected_item")
    item_ok = isinstance(item, dict) and bool(item.get("id"))
    outfit_ok = isinstance(d.get("outfit_suggestion"), str) and bool(d["outfit_suggestion"].strip())
    card_ok = isinstance(d.get("fit_card"), str) and bool(d["fit_card"].strip())
    if group == "matching":
        passed = status == 200 and not error and item_ok and outfit_ok and card_ok
        reason = "complete listing + outfit + fit card" if passed else "incomplete or failed workflow"
    elif group == "zero":
        passed = (status == 200 and error == NO_MATCH and not item_ok and not outfit_ok and not card_ok)
        reason = "correct no-match branch" if passed else "unexpected result/message for a definite no-match request"
    else:
        passed = status == 400 and bool(error) and not item_ok and not outfit_ok and not card_ok
        reason = "400 and rejected before agent" if passed else "invalid body not rejected with HTTP 400"
    if transport_error:
        passed, reason = False, transport_error
    visible_response_proxy = data is not None and transport_error is None
    return {
        "passed_http_proxy": passed,
        "verdict_note": reason,
        "response_within_30s": visible_response_proxy and elapsed <= 30000,
        "error": str(error)[:400] if error is not None else None,
        "selected_item_id": item.get("id") if isinstance(item, dict) else None,
        "outfit_present": outfit_ok,
        "fit_card_present": card_ok,
        "stage_timings_ms_in_response": d.get("stage_timings_ms"),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--group", required=True, choices=("invalid", "zero", "matching"))
    p.add_argument("--phase", default="before", choices=("before", "after1", "after2"))
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--base", default="https://fit-findr.onrender.com/")
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--dry-run", action="store_true", help="preview cases without making requests")
    args = p.parse_args()
    if args.trials < 1:
        p.error("--trials must be at least 1")
    cases = {"matching": MATCHING, "zero": ZERO, "invalid": INVALID}[args.group]
    path = Path("results") / f"capstone_{args.phase}_{args.group}.jsonl"
    summary_path = path.with_suffix(".md")
    print(f"Phase: {args.phase}  Group: {args.group}  Trials: {args.trials}")
    print(f"Target: {args.base}  Cases/trial: {len(cases)}  Total requests: {args.trials * len(cases)}")
    print("Requests are sequential; this is NOT the 10x load test.")
    if args.dry_run:
        for case in cases:
            print(f"  {case[0]}: {case[1]}")
        return
    if path.exists():
        p.error(f"{path} already exists: preserve prior evidence; rename it or choose another phase")
    path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    try:
        with path.open("x", encoding="utf-8") as out:
            for trial in range(1, args.trials + 1):
                for case in cases:
                    case_id, label = case[:2]
                    payload = case[2] if args.group == "invalid" else {"query": label}
                    status, data, elapsed, issue = send(args.base, payload, args.timeout)
                    row = {
                        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
                        "phase": args.phase,
                        "trial": trial,
                        "group": args.group,
                        "case_id": case_id,
                        "case": label,
                        "payload": payload,
                        "http_status": status,
                        "client_elapsed_ms": elapsed,
                        "transport_error": issue,
                        **evaluate(args.group, status, data, elapsed, issue),
                    }
                    records.append(row)
                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out.flush()
                    verdict = "PASS" if row["passed_http_proxy"] else "FAIL"
                    print(f"trial={trial} {case_id} {verdict} HTTP={status} time={elapsed/1000:.2f}s {row['verdict_note']}", flush=True)
    except KeyboardInterrupt:
        print(f"\nInterrupted. Partial evidence preserved: {path}")

    n = len(cases)
    lines = [
        f"# FitFindr capstone {args.phase}: {args.group}", "",
        f"- Hosted endpoint: {args.base.rstrip('/')}/ask",
        f"- Completed HTTP requests: {len(records)} of {args.trials*n}",
        "- Method: sequential HTTP requests from the client; wall-clock durations include network transit",
        "- Limitation: this is an HTTP/API proxy, not an automated browser DOM check",
        "- Limitation: Render's structured server logs and Gemini token counts require independent verification",
        "",
        "| Trial | HTTP proxy passes | Time <= 30s | Criterion outcome |",
        "|---|---:|---:|---|",
    ]
    threshold = {"matching": n, "zero": n, "invalid": n}[args.group]
    for trial in range(1, args.trials+1):
        subset = [r for r in records if r["trial"] == trial]
        passes = sum(r["passed_http_proxy"] for r in subset)
        quick = sum(r["response_within_30s"] for r in subset)
        complete = len(subset) == n
        outcome = "PASS" if complete and passes >= threshold else "MISS / INCOMPLETE"
        lines.append(f"| {trial} | {passes}/{len(subset)} | {quick}/{len(subset)} | {outcome} |")
    if args.group == "matching":
        lines += ["", "For Unit 9 C1: require 10/10 completed outputs per trial and verify actual browser rendering.",
                  "For Unit 9 C5: target >= 9/10 <=30s per trial based on browser-visible latency; HTTP duration here is a proxy."]
    elif args.group == "invalid":
        lines += ["", "For Unit 9 C2: also confirm no MCP stages or Gemini calls ran in server logs.",
                  "Browser may reject empty text before sending a request; test that UI behavior separately."]
    else:
        lines += ["", "For Unit 9 C3: verify the browser displays the broadening message and no listing/card."]
    lines += ["", "## Failures to diagnose", ""]
    for r in records:
        if not r["passed_http_proxy"]:
            lines.append(f"- Trial {r['trial']} {r['case_id']}: HTTP {r['http_status']}, "
                         f"{r['client_elapsed_ms']}ms, {r['verdict_note']}; error={r['error']}")
    if all(r["passed_http_proxy"] for r in records) and records:
        lines.append("- None for the HTTP proxy; browser/log evidence still required.")
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nSaved HTTP evidence: {path}\nSaved summary: {summary_path}")


if __name__ == "__main__":
    main()
