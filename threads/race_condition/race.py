import logging
import threading
import time
from typing import List, Dict

log = logging.getLogger(__name__)

my_store = [
    {
        "id": "foo",
        "status": "pending"
    },
    {
        "id": "bar",
        "status": "pending"
    }
]


my_store_lock = threading.Lock()


def get_pending_object(store: List[Dict[str, str]]) -> List[Dict[str, str]]:
    pending_objects = [e for e in store if e["status"] == "pending"]
    time.sleep(0.5)
    return pending_objects


def handle_object(e: Dict[str, str]) -> None:
    log.info(f"▶ 👷  handle object {e['id']}")
    time.sleep(1)
    e["status"] = "completed"


def lock_object(e: Dict[str, str]) -> bool:
    log.info(f"lock object {e['id']}")
    with my_store_lock:
        if e["status"] == "pending":
            e["status"] = "in_progress"
            return True

    return False


def do_the_job(store: List[Dict[str, str]]) -> None:
    pending_objects = get_pending_object(store)
    log.info(f"found {len(pending_objects)} pending objects to handle...")
    for e in pending_objects:
        if lock_object(e):
            handle_object(e)
        else:
            log.debug(f"✨  object {e['id']} can't be locked, so let's skip it, "
                      f"it has probably be handled by another thread")
