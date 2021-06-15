
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


def run_producer():
    producer = Producer(
        {'bootstrap.servers':'localhost:9092',
        # 'security.protocol' : 'sasl_ssl',
        # 'sasl.mechanism' : 'SCRAM-SHA-512',
        # 'sasl.username' : 'some-user',
        # 'sasl.password' : 'some-password'
        # 'sasl.ca.location': '/home/ebadkamil/kafka...'
        'acks': '-1', # writing to brokers, they acknowledge to producer (0, 1 , -1)
        # 0 No ack, 1 producer will wait until leader replica is written,
        # -1 wait until it receives ack from all replicas/broker,
        'partitioner':'consistent_random'
        }
    )

    kafka_producer = KafkaProducer(producer)
    for i in range(10):
        msg = {
            'id': i,
            'name': Faker('en_US').name()
        }

        kafka_producer.produce(
            'demo',
            str(msg),
            time.time()) # async. Message gets pushed to buffer and returns.


if __name__ == '__main__':
    run_producer()