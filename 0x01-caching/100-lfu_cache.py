#!/usr/bin/env python3
"""LFUCache Module
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """LFUCache defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """

    def __init__(self):
        super().__init__()
        self.cache_lfu = {}
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Add an item in the cache"""
        if key is None or item is None:
            return

        if self.get(key) is not None:
            self.cache_data[key] = item
            return

        if len(self.cache_data) == self.MAX_ITEMS:
            items = list(self.cache_lfu.items())
            least, second_least = items[0], items[1]
            if least[1] == second_least[1]:
                lru = list(self.cache_data.keys())
                least_i = lru.index(least[0])
                second_least_i = lru.index(second_least[0])
                discard = least if least_i < second_least_i else second_least
                self.cache_data.pop(discard[0])
                self.cache_lfu.pop(discard[0])
            else:
                discard = self.cache_data.pop(least[0])
                self.cache_lfu.pop(least[0])

            print(f"DISCARD: {discard[0]}")
        self.cache_data[key] = item
        self.cache_lfu[key] = 1
        self.cache_lfu = dict(
            sorted(self.cache_lfu.items(), key=lambda x: x[1]))

    def get(self, key):
        """Get an item by key"""
        try:
            self.cache_data.move_to_end(key)
            self.cache_lfu[key] += 1
            self.cache_lfu = dict(
                sorted(self.cache_lfu.items(), key=lambda x: x[1]))
        except Exception as exp:
            pass
        return self.cache_data.get(key)
