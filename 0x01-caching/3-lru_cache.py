#!/usr/bin/env python3
"""LRU caching system"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """lru caching"""
    def put(self, key, item):
        """put method"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keys = list(self.cache_data.keys())
                del self.cache_data[keys[0]]
                print(f"DISCARD: {keys[0]}")
            self.cache_data[key] = item

    def get(self, key):
        """get key method"""
        if key is None:
            return None
        if key in self.cache_data:
            temp = self.cache_data.get(key)
            del self.cache_data[key]
            self.cache_data[key] = temp
        return self.cache_data.get(key)
