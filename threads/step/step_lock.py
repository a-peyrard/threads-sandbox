import contextlib
import logging
import threading
from typing import Dict

log = logging.getLogger(__name__)


PRE = 0
INIT = 1
BODY = 2
FINALIZE = 3


class StepContext:
    def __init__(self):
        self.allowed: int = -1
        self.completed: int = -1
        self.lock: threading.Condition = threading.Condition()

    def wait_to_be_allowed_to_enter(self, step: int):
        with self.lock:
            self.lock.wait_for(lambda: step <= self.allowed)

    def wait_to_complete(self, step: int):
        with self.lock:
            self.lock.wait_for(lambda: step <= self.completed)

    def complete(self, step: int):
        with self.lock:
            self.completed = step
            self.lock.notify_all()

    def allow(self, step: int):
        with self.lock:
            self.allowed = step
            self.lock.notify_all()


@contextlib.contextmanager
def in_step(step: int, contexts: Dict[str, StepContext]) -> None:
    ctx = contexts[threading.current_thread().name]
    try:
        log.debug(f"wait to be allowed to enter step #{step}")
        ctx.wait_to_be_allowed_to_enter(step)
        log.debug(f"access granted for step #{step}")
        yield
    finally:
        log.debug(f"notify step #{step} completion")
        ctx.complete(step)


def runnable(contexts: Dict[str, StepContext]) -> None:
    with in_step(INIT, contexts):
        log.info("🖐  We are in INIT step!")

    with in_step(BODY, contexts):
        log.info("🖐  We are in BODY step!")

    with in_step(FINALIZE, contexts):
        log.info("🖐  We are in FINALIZE step!")
