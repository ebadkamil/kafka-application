"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import argparse
import logging
import os.path as osp
import subprocess
import sys
import time

import psutil

from kafka_application.helpers.machine_load_reporter import LoadReporter
from kafka_application.utilities.logger import get_logger


ROOT_PATH = osp.dirname(__file__)


def start_kafka_services(logger):

    zookeeper_exec = osp.join(
        osp.dirname(ROOT_PATH), 'pkg/kafka/kafka/bin/zookeeper-server-start.sh')
    zookeeper_conf = osp.join(
        osp.dirname(ROOT_PATH), 'pkg/kafka/kafka/config/zookeeper.properties')

    process = psutil.Popen(
        [zookeeper_exec, zookeeper_conf])
    time.sleep(10)

    server_exec = osp.join(
        osp.dirname(ROOT_PATH), 'pkg/kafka/kafka/bin/kafka-server-start.sh')
    server_conf = osp.join(
        osp.dirname(ROOT_PATH), 'pkg/kafka/kafka/config/server.properties')
    process = psutil.Popen([server_exec, server_conf])
    time.sleep(5)

    #TODO Add producer, consumer to check if services ran properly
    if process.poll() is None:
        logger.info("Kafka Server is running...")
    else:
        logger.error("Kafka service was terminated ...")
        sys.exit(1)


class Application:
    def __init__(self):
        pass

    def start(self):
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

    #TODO Check if kafka server is already running.
    # start_kafka_services(logger)

    load_reporter = None
    if args.grafana_carbon_address:
        load_reporter = LoadReporter(
            args.grafana_carbon_address, logger,
        )

    try:
        app = Application()
        app.start()
        if load_reporter is not None:
            load_reporter_t = load_reporter.start()

    except KeyboardInterrupt:
        #TODO Handle closing
        load_reporter.stop()

    finally:
        if load_reporter:
            load_reporter_t.join()
