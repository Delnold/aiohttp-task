import logging
from aiohttp import web
from app.middlewares.jwt_middleware import jwt_middleware
from app.routers.iot_devices import setup_iot_routes
from app.routers.auth_router import setup_auth_routes
from app.db.database import database, objects

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])


async def close_database(app):
    await objects.close()
    if not database.is_closed():
        database.close()


app = web.Application(middlewares=[jwt_middleware])
setup_iot_routes(app)
setup_auth_routes(app)
app.on_cleanup.append(close_database)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)
