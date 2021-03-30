"""
Kafka application
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

from functools import wraps
from threading import Thread


def run_in_thread(original):
    @wraps(original)
    def wrapper(*args, **kwargs):
        t = Thread(target=original, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t

    return wrapper
