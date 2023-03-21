import asyncio
from confluent_kafka import Consumer, KafkaError


async def handle_message(msg):
    print(f'Received message: {msg.value().decode("utf-8")}')
    await asyncio.sleep(1)


async def consume():
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(['my-topic'])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            await asyncio.sleep(0.01)
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition event')
            else:
                print(f'Kafka error: {msg.error()}')
        else:
            asyncio.create_task(handle_message(msg))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())


'''

SYNC versiom

'''

# from confluent_kafka import Consumer, KafkaError

# c = Consumer({
#     'bootstrap.servers': 'localhost:9092',
#     'group.id': 'my-group',
#     'auto.offset.reset': 'earliest'
# })

# c.subscribe(['my-topic'])

# while True:
#     msg = c.poll(1.0)

#     if msg is None:
#         continue
#     if msg.error():
#         if msg.error().code() == KafkaError._PARTITION_EOF:
#             print('End of partition event')
#         else:
#             print(f'Kafka error: {msg.error()}')
#     else:
#         print(f'Received message: {msg.value().decode("utf-8")}')

# c.close()