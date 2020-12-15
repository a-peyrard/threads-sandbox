import logging

import sys
import threading

from threads.race_condition.race import do_the_job, my_store

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)

log = logging.getLogger(__name__)


NB_THREADS = 2


def _create_and_start_thread(idx: int) -> threading.Thread:
    log.debug(f"create thread {idx}")
    thread = threading.Thread(target=do_the_job, args=(my_store,))
    thread.start()
    return thread


def main():
    log.info(f"launch {NB_THREADS} threads doing the same job")
    threads = [
        _create_and_start_thread(idx)
        for idx in range(NB_THREADS)
    ]

    log.info(f"wait for all the threads to complete")
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
