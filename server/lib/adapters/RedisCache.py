from redis import Redis


class RedisCache:
    host = "localhost"
    port = 6379
    db = 0
    _redis = Redis(
                host=host,
                port=port,
                db=db,
                socket_timeout=5,
            )

    def __init__(self):
        pass

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, or None if it does not exist.
        """
        value = self._redis.get(key)
        if value is not None:
            return value
        return None

    def set(self, key, value):
        """Add an item to the cache.

        Args:
            key: The key of the item to add.
            value: The value of the item to add.
        """
        self._redis.set(key, value)

    def delete(self, key):
        """Delete an item from the cache.

        Args:
            key: The key of the item to delete.
        """
        self._redis.delete(key)

    def exists(self, key):
        """Check if an item exists in the cache.

        Args:
            key: The key of the item to check.

        Returns:
            True if the item exists, False otherwise.
        """
        return self._redis.exists(key)

    def clear(self):
        """Clear all items from the cache."""
        self._redis.flushall()