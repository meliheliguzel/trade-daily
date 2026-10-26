import json
import os
from pathlib import Path


class ReadWrite:

    def json_write(file_path: str, value: dict | list | tuple) -> None:
        """saves the dictionary to a json file
        Args:
            file_name (_str_):name of the file to be written
            value (_dict_): dictionary to write
        """

        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(value, f)

    def json_read(file_path: str) -> dict | list | tuple:
        """Reads dictionary written in json file

        Args:
            file_name (_str_): _json file name to read_

        Returns:
            _type_: _dict_
        """
        if Path(file_path).is_file() and os.path.getsize(file_path) > 0:
            with open(file_path) as f:

                dictionary = json.load(f)

            return dictionary
        else:
            return None
