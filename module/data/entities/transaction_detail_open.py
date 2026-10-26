from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class TransactionDetailOpen(DbEntity):
    primary_key:int
    transaction_id:int
    entry_price:float
    target_price:float
    stop_price:float
