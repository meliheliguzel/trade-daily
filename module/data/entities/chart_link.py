from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class ChartLink(DbEntity):
    primary_key:int
    transaction_id:int
    link:str
