import jwt
from aiohttp import web
from datetime import datetime, timedelta
from app.core.config import auth_settings


def create_jwt_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, auth_settings.jwt_secret_ket, algorithm="HS256")
    return token

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, auth_settings.jwt_secret_ket, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise web.HTTPUnauthorized(reason="Token has expired")
    except jwt.InvalidTokenError:
        raise web.HTTPUnauthorized(reason="Invalid token")