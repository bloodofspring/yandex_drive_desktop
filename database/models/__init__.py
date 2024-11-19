from database.models.users import AppUser, AppUserConfig
from database.models.storage import FileDirectory, File
from database.models.sessions import Session

active_models = [
    AppUser,
    AppUserConfig,

    FileDirectory,
    File,

    Session,
]
