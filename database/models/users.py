from peewee import CharField, ForeignKeyField

from database.models.base import BaseModel


class AppUserConfig(BaseModel):
    password = CharField()
    yandex_api_key = CharField()


class AppUser(BaseModel):
    login = CharField()
    config = ForeignKeyField(AppUserConfig, backref="user")
