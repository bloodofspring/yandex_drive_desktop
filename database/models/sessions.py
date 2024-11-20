from peewee import ForeignKeyField

from database.models.users import AppUser
from database.models.base import BaseModel


class Session(BaseModel):
    user = ForeignKeyField(AppUser)
