from asyncio import get_running_loop
from functools import wraps, partial


def is_instance_or_subclass(val, class_) -> bool:
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        event_loop = loop or get_running_loop()

        p_func = partial(func, *args, **kwargs)
        return await event_loop.run_in_executor(executor, p_func)

    return run
