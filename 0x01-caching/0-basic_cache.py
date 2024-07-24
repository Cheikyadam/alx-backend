#!/usr/bin/env python3
"""basic caching system"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """basic caching"""
    def put(self, key, item):
        """put method"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """get key method"""
        if key is None:
            return None
        return self.cache_data.get(key)
