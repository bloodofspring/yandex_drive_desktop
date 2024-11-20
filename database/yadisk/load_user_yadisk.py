from typing import Final

import yadisk
from yadisk.exceptions import PathNotFoundError

from database.models import Session, AppUser, File, FileDirectory


class YaDiskDownloader:
    def __init__(self, session: Session):
        self.db_user: AppUser = session.user
        self.yadisk_client: Final[yadisk.YaDisk] = yadisk.YaDisk(self.db_user.config.yandex_api_key)
        self.is_token_valid = self.yadisk_client.check_token()

    def directory_exist(self, name: str, path: str) -> bool:
        return FileDirectory.get_or_none(name=name, path=path, owner=self.db_user) is not None

    def file_exist(self, name: str, path: str) -> bool:
        file: File | None = File.get_or_none(name=name, owner=self.db_user)

        if file is None:
            return False

        return file.path == path

    def update_data(self, current_dir):
        try:
            dirs = tuple(self.yadisk_client.listdir(current_dir.path))
        except PathNotFoundError:
            print("cannot find path:", current_dir.path)
            return

        for o in dirs:
            if o.type != "dir":
                if self.file_exist(name=o.name, path=o.path):
                    continue

                File.create(name=o.name, directory=current_dir)
                continue

            if self.directory_exist(name=o.name, path=o.path):
                continue

            new_dir = FileDirectory.create(name=o.name, path=o.path)
            self.update_data(current_dir=new_dir)

    def load_user_yadisk(self) -> bool:
        if not self.is_token_valid:
            return False

        if self.directory_exist(name="root", path="disk:/"):
            start_dir = FileDirectory.get(name="root", path="disk:/", owner=self.db_user)
            print("[#] updating data...")
        else:
            start_dir = FileDirectory.create(name="root", path="disk:/")
            print("[!] loading data...")

        self.update_data(current_dir=start_dir)

        return True
