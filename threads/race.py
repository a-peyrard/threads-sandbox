import logging
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


def get_pending_object(store: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        e
        for e in store
        if e["status"] == "pending"
    ]


def handle_object(e: Dict[str, str]) -> None:
    log.info(f"▶ 👷  handle object {e['id']}")
    time.sleep(2)
    e["status"] = "completed"


def lock_object(e: Dict[str, str]) -> bool:
    log.info(f"lock object {e['id']} (currently we are not really locking anything...)")
    return True  # fixme: do a real lock, once this is proved to be failing...


def do_the_job(store: List[Dict[str, str]]) -> None:
    pending_objects = get_pending_object(store)
    log.info(f"found {len(pending_objects)} pending objects to handle...")
    for e in pending_objects:
        if lock_object(e):
            handle_object(e)
