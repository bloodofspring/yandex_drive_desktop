from peewee import CharField, ForeignKeyField, BooleanField

from database.models.base import BaseModel


class AppUserConfig(BaseModel):
    password = CharField()
    yandex_api_key = CharField()
    has_valid_token = BooleanField(default=False)


class AppUser(BaseModel):
    login = CharField()
    config = ForeignKeyField(AppUserConfig, backref="user")
