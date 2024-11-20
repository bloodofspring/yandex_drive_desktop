from peewee import CharField, ForeignKeyField

from database.models import AppUser
from database.models.base import BaseModel


class DataModel(BaseModel):
    name = CharField()
    path = CharField()
    owner = ForeignKeyField(AppUser)


class FileDirectory(DataModel):
    pass


class File(DataModel):
    directory = ForeignKeyField(FileDirectory, backref="files_in")
