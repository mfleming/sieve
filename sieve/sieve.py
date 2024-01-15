#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# An implementation of the SIEVE cache eviction algorithm. SIEVE has two
# desirable properties:
#
# - Lazy promotion
# - Quick demotion
#
# One of the really nice attributes of SIEVE is that it doesn't require
# any locking for cache hits because, unlike LRU, objects do not change
# position. This alone contributes to a 2x increase in throughput
# compared with Python's lru_cache().

from functools import _make_key
from _thread import RLock

def _sieve_wrapper(user_func, maxsize):
    cache = {}
    tail = []
    full = None
    tail[:] = [
        tail, # PREV
        tail, # NEXT
        None, # KEY
        None, # RESULT
        None, # VISITED
    ]
    PREV, NEXT, KEY, RESULT, VISITED = 0, 1, 2, 3, 4

    make_key = _make_key
    cache_get = cache.get
    cache_len = cache.__len__
    lock = RLock()

    hand = tail

    def wrapper(*args, **kwargs):
        nonlocal tail, full, hand
        key = make_key(args, kwargs, typed=False)
        link = cache_get(key)
        if link is not None:
            link[VISITED] = True
            return link[RESULT]

        result = user_func(*args, **kwargs)
        with lock:
            # Cache miss
            if key in cache:
                # another thread might have already computed the value
                pass
            elif full:
                o = hand
                if o[KEY] is None:
                    o = tail[PREV]

                while o[VISITED]:
                    o[VISITED] = False
                    o = o[PREV]
                    if o[KEY] is None:
                        o = tail[PREV]

                # Evict o
                hand = o[PREV]
                oldkey = o[KEY]
                hand[NEXT] = o[NEXT]
                o[NEXT][PREV] = hand
                del cache[oldkey]

                # Insert at head of linked list
                head = tail[NEXT]
                new_head = [tail, head, key, result, True]
                head[PREV] = tail[NEXT] = cache[key] = new_head
            else:
                # Insert at head of linked list
                head = tail[NEXT]
                new_head = [tail, head, key, result, True]
                head[PREV] = tail[NEXT] = cache[key] = new_head
                full = (cache_len() >= maxsize)


        return result
    return wrapper

def sieve_cache(maxsize=128):
    def wrapper(user_func):
        w = _sieve_wrapper(user_func, maxsize)
        return w
    return wrapper
