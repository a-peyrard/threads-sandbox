import logging
import sys
import threading
import time
from typing import Dict, List
from unittest import TestCase
from unittest.mock import patch

from threads.race_condition.race import do_the_job, handle_object, get_pending_object, lock_object
from threads.step.step_lock import StepContext, in_step

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)


log = logging.getLogger(__name__)


def _create_and_start_thread(name: str, store: List[Dict[str, str]]) -> threading.Thread:
    log.debug(f"create thread {name}")
    thread = threading.Thread(
        name=name,
        target=do_the_job,
        args=(store,)
    )
    thread.start()
    return thread


class TestRace(TestCase):
    def test_should_simulate_race_condition(self):
        # GIVEN
        test_store = [
            {
                "id": "foo",
                "status": "pending"
            },
            {
                "id": "bar",
                "status": "pending"
            }
        ]
        step_fetch = 1
        step_lock = 2
        contexts = {
            "first": StepContext(),
            "second": StepContext()
        }
        _original_fetch = get_pending_object
        _original_lock = lock_object
        _original_handle = handle_object

        def wrap_fetch(store: List[Dict[str, str]]) -> List[Dict[str, str]]:
            with in_step(step_fetch, contexts):
                return _original_fetch(store)

        def wrap_lock(e: Dict[str, str]) -> bool:
            with in_step(step_lock, contexts):
                return _original_lock(e)

        def wrap_handle(e: Dict[str, str]) -> None:
            log.info(f"wait a bit in thread {threading.current_thread().name}, before handling the item {e['id']}")
            time.sleep(0.2)
            _original_handle(e)

        with patch("threads.race_condition.race.get_pending_object", wraps=wrap_fetch), \
             patch("threads.race_condition.race.lock_object", wraps=wrap_lock), \
             patch("threads.race_condition.race.handle_object", wraps=wrap_handle) as wrapped_handle_object:
            # WHEN

            # create two threads
            first_thread = _create_and_start_thread("first", test_store)
            second_thread = _create_and_start_thread("second", test_store)

            # allow both threads to enter fetch and wait for completion
            contexts["first"].allow(step_fetch)
            contexts["second"].allow(step_fetch)
            contexts["first"].wait_to_complete(step_fetch)
            contexts["second"].wait_to_complete(step_fetch)

            # allow first to lock
            contexts["first"].allow(step_lock)
            contexts["first"].wait_to_complete(step_lock)

            # allow second to lock
            contexts["second"].allow(step_lock)
            contexts["second"].wait_to_complete(step_lock)

            first_thread.join()
            second_thread.join()

            # THEN
            self.assertEqual(
                [e["status"] for e in test_store],
                ["completed", "completed"]
            )
            self.assertEqual(wrapped_handle_object.call_count, 2)
