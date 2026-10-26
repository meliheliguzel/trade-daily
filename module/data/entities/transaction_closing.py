from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class TransactionClosing(DbEntity):
    primary_key:int
    transaction_id:int
    date_of_exit:str
    tp_sl:int
    result:float
