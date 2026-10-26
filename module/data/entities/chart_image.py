from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class ChartImage(DbEntity):
    primary_key:int
    transaction_id:int
    image:bytearray
    extension:str
