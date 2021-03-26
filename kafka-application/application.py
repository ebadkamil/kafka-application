"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import argparse
import os
import sys
import time

import psutil
import subprocess


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
        "--command-topic",
        required=True,
        help="<host[:port][/topic]> Kafka broker/topic to listen for commands",
        type=str)

    app = Application()
    app.start_app()


if __name__ == "__main__":
    start_application()