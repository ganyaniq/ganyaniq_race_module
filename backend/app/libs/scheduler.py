from __future__ import annotations
import threading
import time
import traceback
from typing import Callable

class Job:
    """Background job that runs periodically"""
    
    def __init__(self, name: str, every_sec: int, fn: Callable):
        self.name = name
        self.every_sec = every_sec
        self.fn = fn
        self._t = threading.Thread(target=self._run, daemon=True)
        self._running = False
    
    def start(self):
        """Start the background job"""
        if not self._running:
            self._running = True
            self._t.start()
            print(f"[Scheduler] Started job: {self.name} (every {self.every_sec}s)")
    
    def _run(self):
        while self._running:
            try:
                self.fn()
            except Exception:
                print(f"[Scheduler] Error in job {self.name}:")
                traceback.print_exc()
            time.sleep(self.every_sec)

def start_jobs(jobs: list[Job]):
    """Start all background jobs"""
    for j in jobs:
        j.start()
