from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class TransactionDetailClosing(DbEntity):
    primary_key:int
    transaction_id:int
    exit_price:float
