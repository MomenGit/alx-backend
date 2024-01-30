#!/usr/bin/env python3
""" BaseCache Module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key)
