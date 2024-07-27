from peewee import Model, CharField, ForeignKeyField, AutoField
from app.db.database import database


class BaseModel(Model):
    class Meta:
        database = database


class ApiUser(BaseModel):
    id = AutoField()
    name = CharField()
    email = CharField(unique=True)
    password = CharField()


class Location(BaseModel):
    id = AutoField()
    name = CharField()


class Device(BaseModel):
    id = AutoField()
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location_id = ForeignKeyField(Location, null=True, backref='devices', on_delete='CASCADE',
                                  column_name='location_id')
    api_user_id = ForeignKeyField(ApiUser, backref='devices', on_delete='CASCADE', column_name='api_user_id')
