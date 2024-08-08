import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from loguru import logger


async def producer_func(redis, kafka_client: AIOKafkaProducer):
    """Produce hash to Kafka every 10 seconds(changeable) if it exists"""
    await kafka_client.start()
    try:
        logger.info("Hash producing started")
        while True:
            hashes = await redis.lpop("hash_redis_queue", count=10)
            if hashes:
                for hash_ in hashes:
                    hash_: str
                    await kafka_client.send_and_wait("hashes", key=b'hash_link', value=hash_[1:-1].encode())
            else:
                await asyncio.sleep(10)
    except KafkaError as error:
        logger.error(f"Kafka error: {error}")
    except Exception as error:
        logger.error(f"Error from producer: {error}")
    finally:
        await kafka_client.stop()
