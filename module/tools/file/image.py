import os
from pathlib import Path


def image_data(path: str) ->tuple[bytes,str]|None:

    if Path(path).is_file() and os.path.getsize(path) > 0:

        with open(path, "rb") as file:
            image_data: bytes = file.read()
        extention: str = os.path.splitext(path)[1]

        return (image_data, extention)
    else:
        None
