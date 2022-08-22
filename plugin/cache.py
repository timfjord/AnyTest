from functools import lru_cache, wraps

_cache = []


def cache(func):
    func = lru_cache()(func)
    _cache.append(func)

    @wraps(func)
    def wrapper_cache(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper_cache


def clear():
    for func in _cache:
        func.cache_clear()
