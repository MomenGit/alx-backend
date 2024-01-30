#!/usr/bin/env python3
"""FIFOCache Module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def __init__(self):
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) == self.MAX_ITEMS:
            discard = self.queue.pop(0)
            self.cache_data.pop(discard)
            print(f"DISCARD: {discard}")

        self.cache_data[key] = item
        self.queue.append(key)

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key)
