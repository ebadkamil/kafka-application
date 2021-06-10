from confluent_kafka import Producer
from faker import Faker
import numpy as np


def delivery_report(err, msg):
    """
        err:
        msg: has methods like partitions(), headers(), value() etc
    """
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to partition {msg.partition()} - "
              f"Offset : {msg.offset()} "
              f"{msg.value()}")


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
    # topic_info = producer.list_topics()
    # print(topic_info.topics)
    for i in range(10):
        msg = {
            'id': i,
            'name': Faker('en_US').name()
        }
        msg_header = {
            'source': b'Ebad'
        }

        producer.poll(timeout=0) # Poll the producer for events or callbacks
        producer.produce(
            topic='demo-topic',
            value=str(msg),
            # timestamp=current_time by default,
            headers=msg_header,
            on_delivery = delivery_report) # async. Message gets pushed to buffer and returns.

    producer.flush(
        # timeout in seconds
        ) # Wait for all messages in buffer to be delivered. Covenience method
    # that calls poll() until len() of buffer is zero. Return number of messages in


if __name__ == '__main__':
    run_producer()