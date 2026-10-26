from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class ParityEntity(DbEntity):
    primary_key:int
    platform_id:int
    name:str
