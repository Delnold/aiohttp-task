import logging
from aiohttp import web
from pydantic import ValidationError
from app.auth.jwt_token import create_jwt_token
from app.auth.security import generate_password_hash, check_password_hash
from app.models.model import ApiUser
from peewee import IntegrityError
from app.schemas.user import UserRegisterModel, UserLoginModel
from app.utils.decorators import logging_decorator

logger = logging.getLogger(__name__)
@logging_decorator
async def register(request):
    try:
        data = await request.json()
        validated_data = UserRegisterModel(**data)
        hashed_password = generate_password_hash(validated_data.password)
        user = ApiUser.create(
            name=validated_data.name,
            email=validated_data.email,
            password=hashed_password
        )
        token = create_jwt_token(user.id)
        logger.info("User registered: %s", validated_data.email)
        return web.json_response({'token': token}, status=200)
    except ValidationError as e:
        logger.error("Validation error: %s", e.errors())
        return web.json_response({'error': e.errors()}, status=400)
    except IntegrityError:
        logger.error("Email already exists: %s", data['email'])
        return web.json_response({'error': 'Email already exists'}, status=400)
@logging_decorator
async def login(request):
    try:
        data = await request.json()
        validated_data = UserLoginModel(**data)
        user = ApiUser.get(ApiUser.email == validated_data.email)
        if check_password_hash(validated_data.password, user.password):
            token = create_jwt_token(user.id)
            logger.info("User logged in: %s", validated_data.email)
            return web.json_response({'token': token}, status=200)
        else:
            logger.warning("Invalid credentials for: %s", validated_data.email)
            return web.json_response({'error': 'Invalid credentials'}, status=400)
    except ValidationError as e:
        logger.error("Validation error: %s", e.errors())
        return web.json_response({'error': e.errors()}, status=400)
    except ApiUser.DoesNotExist:
        logger.error("User not found: %s", data['email'])
        return web.json_response({'error': 'User not found'}, status=400)

def setup_auth_routes(app):
    app.router.add_post('/login', login)
    app.router.add_post('/register', register)
