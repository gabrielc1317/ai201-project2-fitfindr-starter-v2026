
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from uuid import uuid4

from flask import g, request

LOG_FILE = Path(__file__).parent / "logs" / "capstone_requests.jsonl"


def setup_observability(app):

    @app.before_request
    def start_request():
        if request.path == "/ask":
            g.request_id = uuid4().hex
            g.request_started = perf_counter()

    @app.after_request
    def record_request(response):
        if request.path != "/ask":
            return response

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}

        query = payload.get("query")
        if not isinstance(query, str):
            query = ""

        session = getattr(g, "fitfindr_session", None)
        if not isinstance(session, dict):
            session = {}

        selected = session.get("selected_item") or {}
        error = session.get("error") or getattr(
            g, "fitfindr_exception", None
        )

        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": getattr(g, "request_id", None),
            "input": {
                "query": query[:200],
                "wardrobe_provided": "wardrobe" in payload,
            },
            "output": {
                "http_status": response.status_code,
                "selected_item_id": selected.get("id"),
                "error": error,
                "success": response.status_code == 200 and not error,
            },
            "duration_ms": round(
                (perf_counter() - g.request_started) * 1000, 2
            ),
            "queue_ms": getattr(g, "queue_ms", 0),
            "stages_ms": session.get("stage_timings_ms", {}),
        }

        line = json.dumps(record, ensure_ascii=False)

        try:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with LOG_FILE.open("a", encoding="utf-8") as logfile:
                logfile.write(line + "\n")
        except OSError as exc:
            print(f"Logging error: {exc}", file=sys.stderr)

        # Also capture the record in Render's service logs.
        print(line, flush=True)

        return response
