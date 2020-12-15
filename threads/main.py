"""
Main entry point for the threads sandbox project.
"""
import logging

import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(module)s : "
           "%(lineno)d - %(message)s"
)

log = logging.getLogger(__name__)


def main():
    log.info("nothing interesting to execute here, see examples in sub-modules...")


if __name__ == "__main__":
    main()
