import logging
from aiohttp import web
from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from pydantic import ValidationError
from app.models.model import Device, Location
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.db.database import objects
from app.utils.decorators import logging_decorator, check_authorization

logger = logging.getLogger(__name__)

@logging_decorator
@check_authorization
async def create_device(request):
    user = request['user']
    try:
        data = await request.json()
        device_data = DeviceCreate(**data)
        if device_data.location_id:
            location = await objects.get(Location, id=device_data.location_id)
            if not location:
                return web.json_response({'error': 'Location does not exist'}, status=400)

        device = await objects.create(Device, **device_data.dict(), api_user_id=user['user_id'])
        logger.debug("Created device: %s", device_data.dict())
        return web.json_response(model_to_dict(device), status=201)
    except ValidationError as e:
        logger.error("Validation error: %s", e.errors())
        return web.json_response({'error': e.errors()}, status=400)
    except Location.DoesNotExist:
        logger.error("Location does not exist")
        return web.json_response({'error': 'Location does not exist'}, status=400)
    except IntegrityError as e:
        logger.error("Integrity error: %s", str(e))
        return web.json_response({'error': f'Integrity error: {str(e)}'}, status=400)
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return web.json_response({'error': str(e)}, status=500)

@logging_decorator
@check_authorization
async def read_device(request):
    device_id = request.match_info['id']
    user = request['user']
    try:
        device = await objects.get(Device, id=device_id)
        if str(device.api_user_id) != str(user['user_id']):
            return web.json_response({'error': 'Not authorized to access this device'}, status=403)
        logger.debug("Read device: %s", model_to_dict(device))
        return web.json_response(model_to_dict(device))
    except Device.DoesNotExist:
        logger.error("Device not found: %s", device_id)
        return web.json_response({'error': 'Device not found'}, status=404)

@logging_decorator
@check_authorization
async def update_device(request):
    device_id = request.match_info['id']
    user = request['user']
    try:
        data = await request.json()
        device_data = DeviceUpdate(**data)
        if device_data.location_id:
            location = await objects.get(Location, id=device_data.location_id)
            if not location:
                return web.json_response({'error': 'Location does not exist'}, status=400)

        device = await objects.get(Device, id=device_id)
        if str(device.api_user_id) != str(user['user_id']):
            return web.json_response({'error': 'Not authorized to update this device'}, status=403)
        await objects.execute(Device.update(**device_data.dict(exclude_unset=True)).where(Device.id == device_id))
        device = await objects.get(Device, id=device_id)
        logger.debug("Updated device: %s", model_to_dict(device))
        return web.json_response(model_to_dict(device))
    except ValidationError as e:
        logger.error("Validation error: %s", e.errors())
        return web.json_response({'error': e.errors()}, status=400)
    except Device.DoesNotExist:
        logger.error("Device not found: %s", device_id)
        return web.json_response({'error': 'Device not found'}, status=404)
    except Location.DoesNotExist:
        logger.error("Location does not exist")
        return web.json_response({'error': 'Location does not exist'}, status=400)
    except IntegrityError as e:
        logger.error("Integrity error: %s", str(e))
        return web.json_response({'error': f'Integrity error: {str(e)}'}, status=400)
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        return web.json_response({'error': str(e)}, status=500)

@logging_decorator
@check_authorization
async def delete_device(request):
    device_id = request.match_info['id']
    user = request['user']
    try:
        device = await objects.get(Device, id=device_id)
        if str(device.api_user_id) != str(user['user_id']):
            return web.json_response({'error': 'Not authorized to delete this device'}, status=403)
        await objects.delete(device)
        logger.debug("Deleted device: %s", device_id)
        return web.json_response({'status': 'success'})
    except Device.DoesNotExist:
        logger.error("Device not found: %s", device_id)
        return web.json_response({'error': 'Device not found'}, status=404)

def setup_iot_routes(app):
    app.router.add_post('/device', create_device)
    app.router.add_get('/device/{id}', read_device)
    app.router.add_put('/device/{id}', update_device)
    app.router.add_delete('/device/{id}', delete_device)
