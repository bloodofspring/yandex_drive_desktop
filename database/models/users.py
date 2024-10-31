from peewee import CharField, ForeignKeyField, IntegerField, BooleanField

from database.models.base import BaseModel


class AppUser(BaseModel):
    pass


class AppUserConfig(BaseModel):
    login = CharField()
    password = CharField()
    yandex_api_key = CharField()

    user = ForeignKeyField(AppUser, backref="config")


class FileCat(BaseModel):
    name = CharField()
    if_file_cat_id = IntegerField()  # 0 если расположен в корневой папке
    is_in_catalogue = BooleanField()
    user = ForeignKeyField(AppUser, backref="backref")
