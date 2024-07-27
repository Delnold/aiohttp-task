import logging
from functools import wraps
from aiohttp import web

logger = logging.getLogger(__name__)

def logging_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = args[0]
        logger.info(f"Entering {func.__name__} with {request.method} request to {request.path}")
        try:
            response = await func(*args, **kwargs)
            logger.info(f"Exiting {func.__name__} with status {response.status}")
            return response
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper


def check_authorization(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        user = request.get('user')
        if not user:
            return web.json_response({'error': 'You need to be authorized'}, status=401)
        return await func(request, *args, **kwargs)

    return wrapper
