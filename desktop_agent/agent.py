from __future__ import annotations
import os
from datetime import datetime
from typing import Dict, Any, Tuple

from config import CATEGORIES, DOWNLOADS_DIR, DRY_RUN
from tools import move_file, write_log
from llm_gemini import classify_file

def get_category_for_ext(ext: str) -> str:
    ext = ext.lower().lstrip(".")
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"

def handle_one_file(path: str) -> Tuple[bool, str]:
    base = os.path.basename(path)
    ext = os.path.splitext(base)[1].lower()

    file_info: Dict[str, Any] = {
        "filename": base,
        "extension": ext,
        "size_bytes": os.path.getsize(path),
        "default_category": get_category_for_ext(ext),
        "note": "Classify this file and propose move/rename."
    }

    decision = classify_file(file_info)

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join("outputs", "activity_log.md")

    if decision.get("action") == "skip":
        line = f"- [{ts}] SKIP `{base}` — {decision.get('reason','')}\n"
        write_log(log_path, line, dry_run=DRY_RUN)
        return True, f"Skipped: {base}"

    if decision.get("action") == "move":
        category = decision.get("category", file_info["default_category"])
        new_name = decision.get("new_name", base)

        # ensure extension preserved
        if not new_name.lower().endswith(ext):
            new_name = os.path.splitext(new_name)[0] + ext

        dst_dir = os.path.join(DOWNLOADS_DIR, category)

        ok, msg = move_file(path, dst_dir, new_name=new_name, dry_run=DRY_RUN)
        line = f"- [{ts}] MOVE `{base}` -> `{category}/{new_name}` — ok={ok} — {decision.get('reason','')}\n"
        write_log(log_path, line, dry_run=DRY_RUN)
        return ok, msg

    # fallback
    line = f"- [{ts}] UNKNOWN_DECISION `{base}` — {decision}\n"
    write_log(log_path, line, dry_run=DRY_RUN)
    return False, "Unknown decision returned by LLM."
