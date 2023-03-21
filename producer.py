import asyncio
from confluent_kafka import Producer, KafkaError

async def produce():
    producer_conf = {
        'bootstrap.servers': 'localhost:9092'
    }

    producer = Producer(producer_conf)

    for i in range(1_000_000):
        try:
            producer.produce('my-topic', value=f'message {i}'.encode())
        except BufferError:
            producer.flush()
            producer.produce('my-topic', value=f'message {i}'.encode())

    producer.flush()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(produce())



# import asyncio
# from confluent_kafka import Producer, KafkaError

# async def produce():
#     producer_conf = {
#         'bootstrap.servers': 'localhost:9092'
#     }

#     producer = Producer(producer_conf)

#     for i in range(100_000):
#         producer.produce('my-topic', value=f'message {i}'.encode())

#     producer.flush()

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(produce())