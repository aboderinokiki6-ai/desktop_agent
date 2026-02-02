from __future__ import annotations
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import DOWNLOADS_DIR, DRY_RUN
from agent import handle_one_file

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = event.src_path

        # wait a bit so file finishes downloading
        time.sleep(2)

        # ignore temp/incomplete downloads
        name = os.path.basename(path).lower()
        if name.endswith(".crdownload") or name.endswith(".tmp") or name.endswith(".part"):
            return

        ok, msg = handle_one_file(path)
        print(f"[AGENT] ok={ok} -> {msg}")

def main():
    downloads = os.path.expandvars(DOWNLOADS_DIR)
    print("=== Desktop Agent (LLM + Tools) ===")
    print(f"Watching: {downloads}")
    print(f"DRY_RUN: {DRY_RUN} (set False in config.py to actually move files)")
    print("Tip: download any file now to see the agent react.\n")

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, downloads, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
