"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import argparse
import subprocess

from kafka_application.kafka_helpers.machine_load_reporter import LoadReporter


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
        type=str)

    args = parser.parse_args()

    load_reporter = None
    if args.grafana_carbon_address:
        load_reporter = LoadReporter(
            args.grafana_carbon_address, update_interval_s=1)

    try:
        app = Application()
        app.start_app()
        if load_reporter is not None:
            load_reporter_t = load_reporter.start()

    except KeyboardInterrupt:
        print("Cancelled by user")

    finally:
        if load_reporter:
            load_reporter_t.join()

if __name__ == "__main__":
    start_application()
