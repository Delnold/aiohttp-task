import jwt
from aiohttp import web
from app.auth.jwt_token import decode_jwt_token


@web.middleware
async def jwt_middleware(request, handler):
    auth_header = request.headers.get('Authorization', None)
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            payload = decode_jwt_token(token)
            request['user'] = payload
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise web.HTTPUnauthorized(reason=str(e))
    return await handler(request)
