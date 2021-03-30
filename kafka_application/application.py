"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import argparse
import logging
import subprocess

from kafka_application.kafka_helpers.machine_load_reporter import LoadReporter
from kafka_application.utilities.logger import get_logger


def start_kafka_services():
    pass


class Application:
    def __init__(self):
        start_kafka_services()

    def start_app(self):
        pass


def start_application():
    parser = argparse.ArgumentParser(prog="kafka application")
    parser.add_argument(
        "--grafana-carbon-address",
        required=False,
        help="<host[:port]> Address to the Grafana (Carbon) metrics server",
        type=str,
    )

    _log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    parser.add_argument(
        "--log-level",
        required=False,
        help="",
        choices=[level.upper() for level in _log_levels.keys()],
        type=lambda s: s.upper(),
        default="INFO",
    )

    args = parser.parse_args()

    logger = get_logger("Kafka-application", level=_log_levels[args.log_level])

    load_reporter = None
    if args.grafana_carbon_address:
        load_reporter = LoadReporter(
            args.grafana_carbon_address, logger,
        )

    try:
        app = Application()
        app.start_app()
        if load_reporter is not None:
            load_reporter_t = load_reporter.start()

    except KeyboardInterrupt:
        load_reporter.stop()

    finally:
        if load_reporter:
            load_reporter_t.join()


if __name__ == "__main__":
    start_application()
