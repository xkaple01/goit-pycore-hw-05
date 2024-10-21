from collections.abc import Callable


def caching_fibonacci() -> Callable[[int], int]:
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]

        cache[n] = fibonacci(n=n - 1) + fibonacci(n=n - 2)
        return cache[n]

    return fibonacci


fibonacci: Callable[[int], int] = caching_fibonacci()