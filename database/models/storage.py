from peewee import CharField, ForeignKeyField

from database.models import AppUser
from database.models.base import BaseModel


class FileDirectory(BaseModel):
    name = CharField()
    path = CharField()
    owner = ForeignKeyField(AppUser, backref="directories")


class File(BaseModel):
    name = CharField()
    directory = ForeignKeyField(FileDirectory, backref="files_in")

    @property
    def path(self):
        return self.directory.path + "/" + self.name
