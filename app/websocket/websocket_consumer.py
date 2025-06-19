import json
from redis.asyncio import Redis  # Modern redis-py async client

from app.constants.constant_strings import ConstantStrnigs
from app.websocket.websocket_router import manager
from app.config.settings import Settings



settings = Settings()


async def websocket_consumer():
    print("consumer_started")
    redis = Redis.from_url(settings.REDIS_URL)
    try:
        async with redis.pubsub() as pubsub:
            await pubsub.subscribe(ConstantStrnigs.MULTIPLIER_CHANNEL.value)

            print(f"channnnnel:{ConstantStrnigs.MULTIPLIER_CHANNEL.value}")
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        print(f"Broadcasting game data: {data}")
                        await manager.broadcast_game_data(data)
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON: {e}")
    finally:
        await redis.close()
