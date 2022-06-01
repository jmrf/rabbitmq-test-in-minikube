import argparse
import json
import logging
import sys
import time

from maipy import logger
from maipy.channels.rabbit import BlockingQueueConsumer, BlockingQueuePublisher
from maipy.io import init_logger
from pika import exchange_type


def on_event(event):
    print(f"Received an event: {event}")


def on_done():
    print("Completed! ")


def get_args():
    parser = argparse.ArgumentParser()
    OP_CHOICES = ["publish", "consume"]
    parser.add_argument(
        "op", choices=OP_CHOICES, help=f"Operation to perform. One of {OP_CHOICES}"
    )
    parser.add_argument(
        "-p",
        "--packets",
        type=int,
        default=10,
        help=f"How many packets for the publish OP to be sent",
    )
    parser.add_argument("--amqp_uri", default="localhost", help="AMQP URI")
    # publisher
    parser.add_argument(
        "--queue",
        "-q",
        help="Bind to a queue to monitor the number of non ACK messages",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=-1,
        help="Max items in the queue before sending",
    )
    parser.add_argument(
        "--to_exchange",
        "-x",
        action="store_true",
        help="whether to publish to an exchange or to a queue directly",
    )
    parser.add_argument("--topic", "-t", help="topic as a routing key")

    return parser.parse_args()


def consumer(args):
    try:
        exchange_name = "maipy-test" if args.to_exchange else ""
        exchange_type = "topic" if args.to_exchange else None
        routing_keys = [f"maipy.test.{args.topic}"] if args.to_exchange else None

        if args.to_exchange and not args.topic:
            raise ValueError(
                f"A topic must be provided when consuming from an exchange"
            )

        consumer = BlockingQueueConsumer(
            args.amqp_uri,
            on_event,
            on_done,
            json.loads,
            routing_keys=routing_keys,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            queue_name=args.queue,
        )

        consumer.consume()
    except KeyboardInterrupt:
        logger.info(f"Closing connection and unbinding")
        # consumer.unbind()
        consumer.close()


def publisher(args):
    if args.to_exchange and not args.topic:
        raise ValueError(f"A topic must be provided when consuming from an exchange")

    exchange_name = "maipy-test" if args.to_exchange else ""
    exchange_type = "topic" if args.to_exchange else None

    # For the Q limit to work, a consumer **must** have declared the queue
    # and bind it to the routing-key the publisher is sending to
    pub = BlockingQueuePublisher(
        args.amqp_uri,
        queue_name=args.queue,
        q_lim=int(args.limit),
        exchange_name=exchange_name,
        exchange_type="topic",
    )

    topic = f"maipy.test.{args.topic}" if args.to_exchange else args.queue

    for i in range(args.packets):
        logger.info(f"Sending message with topic: {topic}")
        pub.send_message(json.dumps({f"hey {i}": f"there {i}"}), topic=topic)
        time.sleep(2)


if __name__ == "__main__":

    args = get_args()

    init_logger(level=logging.DEBUG, logger=logger)

    if args.op == "publish":
        publisher(args)
    elif args.op == "consume":
        consumer(args)
    else:
        raise ValueError("OP argument must be 'consume' or 'publish'")
