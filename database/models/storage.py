from peewee import CharField, ForeignKeyField

from database.models.users import AppUser
from database.models.base import BaseModel


class DataModel(BaseModel):
    name = CharField()
    path = CharField()
    owner = ForeignKeyField(AppUser)

    @property
    def full_way(self):
        return self.path + (self.name if self.name != "root" else "")


class FileDirectory(DataModel):
    pass


class File(DataModel):
    directory = ForeignKeyField(FileDirectory, backref="files_in")
