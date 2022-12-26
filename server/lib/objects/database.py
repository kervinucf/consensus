from server.lib.adapters.MongoDB import MongoDB


class DatabaseObject:
    def __init__(self, database_adapter):
        self.database = database_adapter

    def get(self, key):
        """Retrieve an item from the database by key.

        Args:
            key: The key of the item to retrieve.

        Returns:
            The value of the item if it exists, or None if it does not exist.
        """
        return self.database.get(key)

    def set(self, key, value):
        """Add an item to the database.

        Args:
            key: The key of the item to add.
            value: The value of the item to add.
        """
        self.database.set(key, value)

    def delete(self, key):
        """Delete an item from the database.

        Args:
            key: The key of the item to delete.
        """
        self.database.delete(key)

    def clear(self):
        """Clear all items from the database."""
        self.database.clear()

    def entry_exists(self, key):
        """Check if an entry with the given key exists in the database.

        Args:
            key: The key to check for.

        Returns:
            True if an entry with the given key exists, False otherwise.
        """
        return self.database.entry_exists(key)

