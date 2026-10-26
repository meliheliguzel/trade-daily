from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class PlatformEntity(DbEntity):
    primary_key:int
    name:str
