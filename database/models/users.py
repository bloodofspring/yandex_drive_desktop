from peewee import CharField, ForeignKeyField

from database.models.base import BaseModel


class FileDirectory(BaseModel):
    name = CharField()
    path = CharField()

class File(BaseModel):
    name = CharField()
    directory = ForeignKeyField(FileDirectory, backref="files_in")

    @property
    def path(self):
        return self.directory.path + "/" + self.name


class AppUser(BaseModel):
    pass


class AppUserConfig(BaseModel):
    login = CharField()
    password = CharField()
    yandex_api_key = CharField()
    disk_data_root_folder = ForeignKeyField(FileDirectory, backref="user")

    user = ForeignKeyField(AppUser, backref="config")
