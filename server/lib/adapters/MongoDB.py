from pymongo import MongoClient


class MongoDB:
    def __init__(self, host='localhost', port=27017):
        self.client = MongoClient(host, port)
        self._db = self.client.database

    def get(self, key):
        """Retrieve an item from the database by key.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, or None if it does not exist.
        """
        result = self._db.items.find_one({'key': key})
        if result is not None:
            return result['value']
        return None

    def get_many(self, keys):
        """Retrieve multiple items from the database by keys.

        Args:
            keys: A list of keys to retrieve.

        Returns:
            A list of values for the items with the given keys.
        """
        results = self._db.items.find({'key': {'$in': keys}})
        values = []
        for result in results:
            values.append(result['value'])
        return values

    def set(self, key, value):
        """Add an item to the database.

        Args:
            key: The key of the item to add.
            value: The value of the item to add.
        """
        self._db.items.insert_one({'key': key, 'value': value})

    def set_many(self, items):
        """Add multiple items to the database.

        Args:
            items: A list of key-value pairs to add.
        """
        items_to_insert = []
        for key, value in items:
            items_to_insert.append({'key': key, 'value': value})
        self._db.items.insert_many(items_to_insert)

    def delete(self, key):
        """Delete an item from the database.

        Args:
            key: The key of the item to delete.
        """
        self._db.items.delete_one({'key': key})

    def delete_many(self, keys):
        """Delete multiple items from the database by keys.

        Args:
            keys: A list of keys to delete.
        """
        self._db.items.delete_many({'key': {'$in': keys}})

    def clear(self):
        """Clear all items from the database."""
        self._db.items.delete_many({})

    def entry_exists(self, key):
        """Check if an entry with the given key exists in the database.

        Args:
            key: The key to check for.

        Returns:
            True if an entry with the given key exists, False otherwise.
        """
        result = self._db.items.find_one({'key': key})
        return result is not None
