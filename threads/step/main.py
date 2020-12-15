import logging

import sys
import threading
import time
from typing import Dict

from threads.step.step_lock import StepContext, runnable, Step

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)

log = logging.getLogger(__name__)


def _create_and_start_thread(name: str, contexts: Dict[str, StepContext]) -> threading.Thread:
    log.debug(f"create thread {name}")
    thread = threading.Thread(
        name=name,
        target=runnable,
        args=(contexts,)
    )
    thread.start()
    return thread


def main():
    log.info("create some initial context")
    contexts = {
        "first": StepContext(),
        "second": StepContext()
    }
    log.info("launch the threads")
    first_thread = _create_and_start_thread("first", contexts)
    second_thread = _create_and_start_thread("second", contexts)

    log.info("sleep a bit...")
    time.sleep(0.5)

    log.info("allow INIT for first thread and wait for completion")
    contexts["first"].allow(Step.INIT)
    contexts["first"].wait_to_complete(Step.INIT)

    log.info("sleep a bit...")
    time.sleep(0.5)

    log.info("allow BODY for first and wait for completion, and allow INIT for second")
    contexts["first"].allow(Step.BODY)
    contexts["first"].wait_to_complete(Step.BODY)
    contexts["second"].allow(Step.INIT)
    contexts["second"].wait_to_complete(Step.INIT)

    log.info("sleep a bit...")
    time.sleep(0.5)

    log.info("allow FINALIZE for first and wait for completion")
    contexts["first"].allow(Step.FINALIZE)
    contexts["first"].wait_to_complete(Step.FINALIZE)

    log.info("allow BODY for second and wait for completion")
    contexts["second"].allow(Step.BODY)
    contexts["second"].wait_to_complete(Step.BODY)
    log.info("allow FINALIZE for second and wait for completion")
    contexts["second"].allow(Step.FINALIZE)
    contexts["second"].wait_to_complete(Step.FINALIZE)

    log.info(f"wait for all the threads to complete")
    first_thread.join()
    second_thread.join()


if __name__ == "__main__":
    main()
