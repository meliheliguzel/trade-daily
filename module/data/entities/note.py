from dataclasses import dataclass

from .base_entity import DbEntity


@dataclass
class Note(DbEntity):
    primary_key:int
    transaction_id:int
    note_text:str
