from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class StrategyEntity(DbEntity):
    primary_key:int
    name:str
    description:str
