"""
Main entry point for the gitapi server.
"""
import logging

import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)

log = logging.getLogger(__name__)


def main():
    log.info("foobar")


if __name__ == "__main__":
    main()
