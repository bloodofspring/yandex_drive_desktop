from peewee import SqliteDatabase
from typing import Final

db: Final[SqliteDatabase] = SqliteDatabase("app_database")
