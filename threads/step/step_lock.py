import contextlib
import logging
import threading
from enum import Enum
from typing import Dict

log = logging.getLogger(__name__)


class Step(Enum):
    PRE = 0
    INIT = 1
    BODY = 2
    FINALIZE = 3


class StepContext:
    def __init__(self):
        self.allowed: Step = Step.PRE
        self.completed: Step = Step.PRE
        self.lock: threading.Condition = threading.Condition()

    def wait_to_be_allowed_to_enter(self, step: Step):
        with self.lock:
            self.lock.wait_for(lambda: step.value <= self.allowed.value)

    def wait_to_complete(self, step: Step):
        with self.lock:
            self.lock.wait_for(lambda: step.value <= self.completed.value)

    def complete(self, step: Step):
        with self.lock:
            self.completed = step
            self.lock.notify_all()

    def allow(self, step: Step):
        with self.lock:
            self.allowed = step
            self.lock.notify_all()


@contextlib.contextmanager
def in_step(step: Step, contexts: Dict[str, StepContext]) -> None:
    ctx = contexts[threading.current_thread().name]
    try:
        log.debug(f"wait to be allowed to enter {step}")
        ctx.wait_to_be_allowed_to_enter(step)
        log.debug(f"access granted for {step}")
        yield
    finally:
        log.debug(f"notify {step} completion")
        ctx.complete(step)


def runnable(contexts: Dict[str, StepContext]) -> None:
    with in_step(Step.INIT, contexts):
        log.info("🖐  We are in INIT step!")

    with in_step(Step.BODY, contexts):
        log.info("🖐  We are in BODY step!")

    with in_step(Step.FINALIZE, contexts):
        log.info("🖐  We are in FINALIZE step!")
