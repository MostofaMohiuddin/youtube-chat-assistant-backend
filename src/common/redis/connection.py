import redis
from redis import Redis
from typing import Optional


class RedisConnection:
    _instance: Optional[Redis] = None
    _initialized: bool = False

    @classmethod
    def get_instance(cls) -> Redis:
        """
        Get singleton instance of Redis connection.

        Returns:
            Redis: A Redis client instance
        """
        if cls._instance is None:
            cls._instance = cls._create_connection()

        return cls._instance

    @classmethod
    def _create_connection(cls) -> Redis:
        """
        Create a new Redis connection.

        Returns:
            Redis: A new Redis client instance
        """

        try:
            client = redis.Redis(
                host="your_redis_host",
                port=13447,
                decode_responses=True,
                username="default",
                password="your_redis_password",
            )
            # Test connection
            client.ping()
            return client
        except redis.RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis: {str(e)}") from e

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the Redis connection explicitly.
        Useful for startup checks and events.
        """
        if not cls._initialized:
            cls.get_instance()
            cls._initialized = True

    @classmethod
    def close(cls) -> None:
        """
        Close the Redis connection.
        """
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None
            cls._initialized = False
