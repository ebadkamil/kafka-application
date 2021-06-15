
from threading import Thread
import time

from faker import Faker
from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self, producer):
        self._producer = producer
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.5)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()
        max_wait_to_publish_producer_queue = 2
        self._producer.flush(max_wait_to_publish_producer_queue)

    def produce(
        self,
        topic,
        payload,
        timestamp,
    ):
        def ack(err, msg):
            if err:
                print(f"Message failed delivery: {err}")
            else:
                print(f"Message delivered to partition {msg.partition()} - "
                      f"Offset : {msg.offset()} "
                      f"{msg.value()}")
        try:
            self._producer.produce(
                topic, payload, on_delivery=ack, timestamp=timestamp
            )
        except Exception as ex:
            print(f"Kafka message could not be published: {ex}")
        self._producer.poll(0)
