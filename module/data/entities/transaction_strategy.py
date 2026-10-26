from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class TransactionStrategy(DbEntity):
    primary_key:int
    transaction_id:int
    strategy_id:int
    name:str
