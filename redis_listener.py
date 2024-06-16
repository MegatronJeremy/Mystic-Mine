from configuration import Configuration
from courier import banned
from redis import Redis
from threading import Thread

import time


def listener():
    redis_client = Redis(
        host=Configuration.REDIS_HOST, port=Configuration.REDIS_PORT, db=0)
    pubsub = redis_client.pubsub()
    pubsub.subscribe(Configuration.REDIS_CHANNEL)

    print("GOT IT")

    first = True
    for message in pubsub.listen():
        if first:
            first = False
            continue

        # Only decode if the message data is of type bytes
        if isinstance(message["data"], bytes):
            username = message["data"].decode()
            banned.append(username)
        else:
            print(f"Received non-byte message: {message}")


if (__name__ == "__main__"):
    done = False
    while (not done):
        try:
            with Redis(host=Configuration.REDIS_HOST, port=Configuration.REDIS_PORT, db=0) as redis:
                list = redis.lrange(Configuration.REDIS_BUFFER, 0, -1)
                banned = [item.decode() for item in list]

            print(banned)

            done = True
        except Exception as error:
            print(error)
            time.sleep(1)

    Thread(target=listener).start()
