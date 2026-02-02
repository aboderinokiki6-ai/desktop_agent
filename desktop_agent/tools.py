from __future__ import annotations
import os
import shutil
import re
from datetime import datetime
from typing import Tuple

def ensure_dir(path: str) -> Tuple[bool, str]:
    try:
        os.makedirs(path, exist_ok=True)
        return True, path
    except Exception as e:
        return False, f"ensure_dir error: {e}"

def safe_name(name: str) -> str:
    name = re.sub(r"[^\w\-. ]+", "_", name).strip()
    name = re.sub(r"\s+", " ", name)
    return name[:180]

def move_file(src: str, dst_dir: str, new_name: str | None = None, dry_run: bool = True) -> Tuple[bool, str]:
    if not os.path.exists(src):
        return False, "Source file not found."

    ok, msg = ensure_dir(dst_dir)
    if not ok:
        return False, msg

    base = os.path.basename(src)
    target_name = safe_name(new_name) if new_name else base
    dst = os.path.join(dst_dir, target_name)

    # avoid overwrite
    if os.path.exists(dst):
        stem, ext = os.path.splitext(target_name)
        dst = os.path.join(dst_dir, f"{stem}_{int(datetime.now().timestamp())}{ext}")

    if dry_run:
        return True, f"DRY_RUN: would move '{src}' -> '{dst}'"

    try:
        shutil.move(src, dst)
        return True, f"Moved '{src}' -> '{dst}'"
    except Exception as e:
        return False, f"move_file error: {e}"

def write_log(path: str, content: str, dry_run: bool = True) -> Tuple[bool, str]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if dry_run:
        return True, f"DRY_RUN: would write log to {path}"
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return True, f"Wrote log to {path}"
    except Exception as e:
        return False, f"write_log error: {e}"
