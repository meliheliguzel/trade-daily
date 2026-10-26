from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class Balance(DbEntity):
    primary_key:int
    transaction_id:int
    size_id:int
    value:float
    estimated:float

@dataclass
class BalanceSize(DbEntity):
    primary_key:int
    size:float
    state:int

