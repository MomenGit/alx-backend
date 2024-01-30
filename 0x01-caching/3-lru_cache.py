#!/usr/bin/env python3
"""LRUCache Module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def __init__(self):
        super().__init__()
        self.lru = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if self.get(key) is not None:
            self.cache_data[key] = item
            return

        if len(self.cache_data) == self.MAX_ITEMS:
            discard = self.lru.pop(0)
            self.cache_data.pop(discard)
            print(f"DISCARD: {discard}")

        self.cache_data[key] = item
        self.lru.append(key)

    def get(self, key):
        """Get an item by key"""
        try:
            self.lru.remove(key)
            self.lru.append(key)
        except Exception:
            pass
        return self.cache_data.get(key)
