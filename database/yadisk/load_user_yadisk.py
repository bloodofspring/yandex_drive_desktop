from typing import Final

import yadisk
from yadisk.exceptions import PathNotFoundError

from database.models import Session, AppUser, File, FileDirectory


def load_data(yadisk_client: yadisk.YaDisk, current_dir):
    try:
        dirs = tuple(yadisk_client.listdir(current_dir.path))
    except PathNotFoundError:
        print("cannot find:", current_dir.path)
        return

    for o in dirs:
        if o.type != "dir":
            File.create(name=o.name, directory=current_dir)
            continue

        new_dir = FileDirectory.create(name=o.name, path=o.path)
        load_data(yadisk_client=yadisk_client, current_dir=new_dir)


def load_user_yadisk(session: Session) -> bool:
    db_user: AppUser = session.user
    yadisk_instance: Final[yadisk.YaDisk] = yadisk.YaDisk(db_user.config.yandex_api_key)

    if not yadisk_instance.check_token():
        return False

    load_data(current_dir=FileDirectory.create(name="root", path="disk:/"))

    return True
