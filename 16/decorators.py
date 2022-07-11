import datetime
import functools
import typing as tp


def call_n_times(n: int) -> tp.Callable:

    def call_n_times_decorator(foo: tp.Callable) -> tp.Callable:

        @functools.wraps(foo)
        def foo_called_n_times(*args, **kwargs):
            for _ in range(n):
                foo(*args, **kwargs)

        return foo_called_n_times

    return call_n_times_decorator


call_3_times = call_n_times(n=3)


# @call_3_times
@call_n_times(n=2)
def print_time(message: str) -> None:
    """
    Prints current time prepended with a message.
    """
    print(f"{message} '{datetime.datetime.now()}'")


assert isinstance(print_time, object)
#print_time("Current time is")

#print(f"{print_time.__name__ = }")
#print(f"{print_time.__doc__ = }")

call_6_times = call_3_times(print_time)


i = 0


def cache(foo):
    cache = {}
    @functools.wraps(foo)
    def wrapped(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        try:
            foo_result = cache[cache_key]
            print(f"found in cache: {cache_key}")
        except KeyError:
            foo_result = foo(*args, **kwargs)
            cache[cache_key] = foo_result
        return foo_result
    return wrapped


@functools.lru_cache(maxsize=3)
def fibonacci(n: int) -> int:
    """
    Returns n-th Fibonacci number.
    """
    global i
    i += 1
    print(f"Call to fib: {n} ({i})")

    return fibonacci(n - 1) + fibonacci(n - 2) if n > 1 else n


print(fibonacci(8))

print(fibonacci(9))
