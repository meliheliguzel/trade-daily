import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from config import Locations, UserLocations
from module.data.connection import create_new_user_db
from module.data.settings.data import IDataEntity
from module.tools.file import ReadWrite


@dataclass
class UsersEntity(IDataEntity):

    CURRENT_USER: str
    USER_LIST: list[str]


class UsersManager:

    def __init__(self) -> None:

        self.data: UsersEntity = None
        self.load()

    def validate_name(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        name = name.strip()
        if len(name) < 2 or len(name) > 30:
            return False

        if not re.match(r"^[a-zA-Z0-9_\-]+$", name):
            return False
        reserved_names = {"con", "prn", "aux", "nul", "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9", "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"}
        if name.lower() in reserved_names:
            return False
        return True

    def add(self, name: str) -> None:
        if not self.validate_name(name):
            raise ValueError(
                f"Invalid account name: '{name}'. Only letters, numbers, underscore (_), and hyphen (-) are allowed. Length must be between 2 and 30 characters."
            )

        if name not in self.data.USER_LIST:
            user_loc = Path(self.__get_user_path(name))
            user_loc.mkdir(parents=True, exist_ok=True)

            db_path = str(user_loc / "default.db")
            create_new_user_db(db_path)

            if not self.data:
                self.data = UsersEntity(name, [name])
            else:
                self.data.USER_LIST.append(name)
            self.save()

    def update(self, old_user: str, new_user: str) -> bool:
        if not self.validate_name(new_user):
            raise ValueError(
                f"Invalid account name: '{new_user}'. Only letters, numbers, underscore (_), and hyphen (-) are allowed. Length must be between 2 and 30 characters."
            )
        if new_user in self.data.USER_LIST:
            raise ValueError(f"Account name is already in use: '{new_user}'")

        if old_user in self.data.USER_LIST:
            index: int = self.data.USER_LIST.index(old_user)
            self.data.USER_LIST[index] = new_user
            os.rename(self.__get_user_path(old_user), self.__get_user_path(new_user))
            if self.data.CURRENT_USER == old_user:
                self.data.CURRENT_USER = new_user
            self.save()
            return True
        return False

    def remove(self, user: str) -> bool:

        user_path: str = self.__get_user_path(user)
        if user in self.data.USER_LIST and os.path.exists(user_path):
            self.data.USER_LIST.remove(user)
            shutil.rmtree(user_path)
            if self.data.CURRENT_USER == user:
                if len(self.data.USER_LIST):
                    self.data.CURRENT_USER = self.data.USER_LIST[0]
                else:
                    self.add("main")
            self.save()
            return True
        return False

    def set_current_user(self, user: str) -> bool:

        if user in self.data.USER_LIST:
            self.data.CURRENT_USER = user
            self.save()
            return True
        return False

    def get_user_loc(self) -> UserLocations:
        return UserLocations(self.data.CURRENT_USER)

    def get_user_list(self) -> list[str]:
        return self.data.USER_LIST

    def __get_user_path(self, name: str) -> str:
        return f"{Locations.MAIN}/{name}"


    def save(self) -> None:
        ReadWrite.json_write(Locations.USER_SETUP, self.data.__dict__)

    def load(self) -> None:
        try:
            data_dict: dict | list | tuple = ReadWrite.json_read(Locations.USER_SETUP)
        except Exception:
            data_dict = None

        if data_dict:
            self.data = UsersEntity(**data_dict)
        else:
            self.__new_user()

    def __new_user(self) -> None:

        name = "main"
        user_loc: str = self.__get_user_path(name)
        os.makedirs(user_loc, exist_ok=True)

        db_path = os.path.join(user_loc, "default.db")
        create_new_user_db(db_path)

        self.data = UsersEntity(CURRENT_USER=name, USER_LIST=[name])
        self.save()
