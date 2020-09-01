from functools import wraps, partial


def is_instance_or_subclass(val, class_) -> bool:
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop, executor=None, **kwargs):
        if loop is None:
            raise ValueError("The loop parameter cannot be null. "
                             "Ensure this was passed correctly through the "
                             "wrapped method / function.")

        p_func = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, p_func)

    return run
