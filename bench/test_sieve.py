from sieve.sieve import sieve_cache
from sieve.lru import lru_cache

@sieve_cache(maxsize=128)
def func_sieve(obj):
    return obj

@lru_cache(maxsize=128)
def func_lru(obj):
    return obj

def sieve_cache_test_hit():
    func_sieve(1)

def test_sieve_hit(benchmark):
    benchmark(sieve_cache_test_hit)

def lru_cache_test_hit():
    func_lru(1)

def test_lru_hit(benchmark):
    benchmark(lru_cache_test_hit)

def sieve_cache_test_miss():
    for i in range(1000):
        func_sieve(i)

def test_sieve_miss(benchmark):
    benchmark(sieve_cache_test_miss)

def lru_cache_test_hit():
    func_lru(1)

def lru_cache_test_miss():
    for i in range(1000):
        func_lru(i)

def test_lru_miss(benchmark):
    benchmark(lru_cache_test_miss)
