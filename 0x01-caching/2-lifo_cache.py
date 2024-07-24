#!/usr/bin/env python3
"""LIFO caching system"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """lifo caching"""
    def put(self, key, item):
        """put method"""
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                keys = list(self.cache_data.keys())
                del self.cache_data[keys[len(keys) - 1]]
                print(f"DISCARD: {keys[len(keys) - 1]}")
            self.cache_data[key] = item

    def get(self, key):
        """get key method"""
        if key is None:
            return None
        return self.cache_data.get(key)
