import asyncio

async def retry_async(fn, *args, retries=2, delay=1.5, **kwargs):
    last_err = None
    for attempt in range(retries + 1):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            last_err = e
            if attempt < retries:
                await asyncio.sleep(delay * (attempt + 1))
            else:
                raise last_err