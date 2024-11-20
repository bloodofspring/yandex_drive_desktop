# ToDo: Удалить метод de_id
# ToDo: Переделать клиента в ассинхрон
import os.path
from typing import Final

import yadisk
from yadisk.exceptions import PathNotFoundError

from database.models import Session, AppUser, File, FileDirectory
from database.models.storage import DataModel


class YaDiskDownloader:
    def __init__(self, session: Session):
        self.db_user: AppUser = session.user
        self.yadisk_client: Final[yadisk.YaDisk] = yadisk.YaDisk(token=self.db_user.config.yandex_api_key)
        self.is_token_valid = self.yadisk_client.check_token()

    @classmethod
    def de_id(cls, id_: int):
        return cls(session=Session.create(user=AppUser.get_by_id(id_)))

    def directory_exist(self, name: str, path: str) -> bool:
        return FileDirectory.get_or_none(name=name, path=path, owner=self.db_user) is not None

    def file_exist(self, name: str, path: str) -> bool:
        return File.get_or_none(name=name, path=path, owner=self.db_user) is not None

    def update_data(self, current_dir):
        try:
            dirs = tuple(self.yadisk_client.listdir(current_dir.full_way))
        except PathNotFoundError:
            print("cannot find path:", current_dir.full_way)
            return

        for o in dirs:
            path = o.path.rstrip(o.name)

            if o.type != "dir":
                if self.file_exist(name=o.name, path=path):
                    continue

                File.create(name=o.name, path=path, directory=current_dir, owner=self.db_user)
                continue

            if self.directory_exist(name=o.name, path=path):
                self.update_data(current_dir=FileDirectory.get(name=o.name, path=path, owner=self.db_user))
                continue

            new_dir = FileDirectory.create(name=o.name, path=path, owner=self.db_user)
            self.update_data(current_dir=new_dir)

    def load_user_yadisk(self) -> bool:
        if not self.is_token_valid:
            return False

        if self.directory_exist(name="root", path="disk:/"):
            start_dir = FileDirectory.get(name="root", path="disk:/", owner=self.db_user)
            print("[#] updating data...")
        else:
            start_dir = FileDirectory.create(name="root", path="disk:/", owner=self.db_user)
            print("[!] loading data...")

        self.update_data(current_dir=start_dir)

        return True

    def get_path_data(self, path: str) -> tuple[DataModel]:
        files = File.select().where(
            (File.path == path) & (File.owner == self.db_user)
        )[:]
        directories = FileDirectory.select().where(
            (FileDirectory.path == path) & (FileDirectory.name != "root") & (FileDirectory.owner == self.db_user)
        )[:]
        result = tuple(files + directories)

        return result

    def download_file(self, way: str) -> str:
        if not os.path.exists("downloaded_materials"):
            os.mkdir("downloaded_materials")

        download_path_name = f"downloaded_materials/{way.rstrip('/').split('/')[-1]}"
        self.yadisk_client.download(way, download_path_name)

        return download_path_name
