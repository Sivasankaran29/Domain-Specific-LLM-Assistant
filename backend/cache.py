from functools import lru_cache

# simple in-memory cache
cache = {}

def get_cache(key):
    return cache.get(key)

def set_cache(key, value):
    cache[key] = value