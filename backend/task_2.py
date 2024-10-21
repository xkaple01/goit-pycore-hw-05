from collections.abc import Generator, Callable


def generator_numbers(text: str) -> Generator[float]:
    for w in text.split(sep=' '):
        try:
            yield float(w)
        except:
            pass


def sum_profit(text: str, func: Callable[[str], Generator[float]]) -> float:
    return sum(func(text))
