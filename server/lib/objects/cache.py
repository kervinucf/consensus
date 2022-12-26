from server.lib.adapters.RedisCache import RedisCache


class CacheObject:
    def __init__(self, cache_adapter=None):

        if cache_adapter is None:
            self._cache = {}
        else:
            self._cache = cache_adapter

    def get(self, key):
        """Retrieve an item from the cache by key.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, or None if it does not exist.
        """
        return self._cache.get(key)

    def set(self, key, value):
        """Add an item to the cache.

        Args:
            key: The key of the item to add.
            value: The value of the item to add.
        """
        self._cache.set(key, value)

    def exists(self, key):
        """Check if an item exists in the cache.

        Args:
            key: The key of the item to check.

        Returns:
            True if the item exists, False otherwise.
        """
        return self._cache.exists(key)

    def delete(self, key):
        """Delete an item from the cache.

        Args:
            key: The key of the item to delete.
        """
        self._cache.delete(key)

    def clear(self):
        """Clear all items from the cache."""
        self._cache.clear()


redis_cache = CacheObject(cache_adapter=RedisCache())
