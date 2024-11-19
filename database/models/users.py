from peewee import CharField, ForeignKeyField

from database.models.base import BaseModel
from database.models.storage import FileDirectory


class AppUser(BaseModel):
    pass


class AppUserConfig(BaseModel):
    login = CharField()
    password = CharField()
    yandex_api_key = CharField()
    disk_data_root_folder = ForeignKeyField(FileDirectory, backref="user")

    user = ForeignKeyField(AppUser, backref="config")
