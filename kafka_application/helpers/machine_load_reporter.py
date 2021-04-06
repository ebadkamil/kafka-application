"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import logging
import os
import sys
import time

import graphyte  # type: ignore
import numpy as np
import psutil as ps

from kafka_application.utilities.utils import run_in_thread


class LoadReporter:
    def __init__(
        self,
        graphyte_server: str,
        logger: logging.Logger,
        prefix: str = "machine_info",
        update_interval_s: int = 10,
    ):
        self._graphyte_server = graphyte_server
        self._logger = logger
        self._update_interval_s = update_interval_s
        self._stop = False
        self._sender = graphyte.Sender(self._graphyte_server, prefix=prefix)

    @run_in_thread
    def start(self):
        while not self._stop:
            timestamp = time.time()
            memory = (ps.virtual_memory()).used / 1024 ** 3
            load = ps.cpu_percent()
            try:
                self._sender.send("cpu_load", load, timestamp)
                self._sender.send("memory", memory, timestamp)
                self._logger.debug(f"load {load}: memory {memory}")
            except Exception as ex:
                self._logger.error(f"Could not send load information: {ex}")
            time.sleep(self._update_interval_s)

    def stop(self):
        self._stop = True
