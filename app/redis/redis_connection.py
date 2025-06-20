
from redis.asyncio import Redis 
from app.config.settings import Settings


settings = Settings()
redis_connection =Redis.from_url(settings.REDIS_URL)
