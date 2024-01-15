# Sieve implementation in Python

[SIEVE](https://cachemon.github.io/SIEVE-website/) is an eviction algorithm
that is simpler and more efficient than FIFO. This project implements a cache
using a Python decorator that uses SIEVE for eviction.

You can use a SIEVE-backed cache in your code with the `@sieve_cache`
decorator.

## Benchmarks

Here's a comparison of SIEVE against the pure Python LRU implementation from
the Python standard library.

```
--------------------------------------------------------------------------------- benchmark: 4 tests ---------------------------------------------------------------------------------
Name (time in ms)        Min               Max              Mean            StdDev            Median               IQR            Outliers  OPS (Kops/s)            Rounds  Iterations
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_sieve_hit        0.0003 (1.0)      0.0018 (1.0)      0.0003 (1.0)      0.0000 (1.0)      0.0003 (1.0)      0.0000 (1.0)    13072;28199    2,974.5402 (1.0)      986760          16
test_lru_hit          0.0005 (1.72)     0.0034 (1.91)     0.0006 (1.69)     0.0000 (1.33)     0.0006 (1.69)     0.0000 (1.55)   15094;24408    1,763.8459 (0.59)     923173          10
test_lru_miss         0.7248 (>1000.0)  1.0644 (594.54)   0.7414 (>1000.0)  0.0093 (397.57)   0.7402 (>1000.0)  0.0092 (>1000.0)   1056;70        1.3489 (0.00)       6911           1
test_sieve_miss       0.7313 (>1000.0)  1.5177 (847.71)   0.7703 (>1000.0)  0.0262 (>1000.0)  0.7678 (>1000.0)  0.0185 (>1000.0)    347;33        1.2981 (0.00)       6863           1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Cache hits are around 2x faster with SIEVE eviction than LRU mainly because of
the fact that SIEVE doesn't take a lock on the hit path.

## References

- [Official SIEVE website](https://cachemon.github.io/SIEVE-website/)
- [NSDI 24 Paper](https://cachemon.github.io/SIEVE-website/)
- [Why aren't we SIEVE'ing?](https://brooker.co.za/blog/2023/12/15/sieve.html)
