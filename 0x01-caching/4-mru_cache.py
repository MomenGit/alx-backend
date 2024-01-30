#!/usr/bin/env python3
"""MRUCache Module
"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if self.get(key) is not None:
            self.cache_data[key] = item
            return

        if len(self.cache_data) == self.MAX_ITEMS:
            discard = self.cache_data.popitem()
            print(f"DISCARD: {discard[0]}")

        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        try:
            self.cache_data.move_to_end(key)
        except Exception as exp:
            pass
        return self.cache_data.get(key)
