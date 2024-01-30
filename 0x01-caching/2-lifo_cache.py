#!/usr/bin/env python3
"""LIFOCache Module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data.keys():
            self.cache_data.pop(key)

        if len(self.cache_data) == self.MAX_ITEMS:
            print(f"DISCARD: {self.cache_data.popitem()[0]}")

        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key)
