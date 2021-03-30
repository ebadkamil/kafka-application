"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import os
import sys
import time
import graphyte  # type: ignore

import psutil

from kafka_application.utilities.utils import run_in_thread


class LoadReporter:
    def __init__(
        self,
        graphyte_server: str,
        prefix: str = "throughput",
        update_interval_s: int = 10,
    ):
        self._graphyte_server = graphyte_server
        self._update_interval_s = update_interval_s

        self._sender = graphyte.Sender(self._graphyte_server, prefix=prefix)

    @run_in_thread
    def start(self):
        while True:
            timestamp = time.time()
            try:
                self._sender.send("cpu_load", load, timestamp)
                self._sender.send("memory", memory, timestamp)
            except Exception as ex:
                print(f"Could not send load information: {ex}")

            time.sleep(self.update_interval_s)
