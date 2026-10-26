from dataclasses import dataclass

from .base_entity import DbEntity


class TransactionDataType:
    TP:int = 1
    SL:int = 0
    LONG:int = 1
    SHORT:int = 0


@dataclass
class Transaction(DbEntity):
    primary_key:int
    platform:str
    parity:str
    date_of_entry:str
    long_short:bool #ii 1 (true,long) 0 false
    rr:float
    size:float
    tp_sl:bool|None #ii 1 (true,tp) 0 false

class TransactionState:
    OPEN:None = None
    TP:bool = True
    SL:bool = False
    OPEN_show:str = "open"
    TP_show:str = "tp"
    SL_show:str = "sl"
    state_read:dict = {TransactionDataType.SL:SL,TransactionDataType.TP:TP}
    state_read_show:dict = {SL:SL_show,TP:TP_show,OPEN:OPEN_show}
    state_write:dict = {SL:TransactionDataType.SL,TP:TransactionDataType.TP}

class TransactionDirection:
    LONG:str = "long"
    SHORT:str = "short"
    direction_read:dict = {TransactionDataType.SHORT:SHORT,TransactionDataType.LONG:LONG}
    direction_write:dict = {SHORT:TransactionDataType.SHORT,LONG:TransactionDataType.LONG}

class TransactionShowData:
    state:dict = {TransactionDataType.SL:TransactionState.SL_show,
                  TransactionDataType.TP:TransactionState.TP_show}
    OPEN:str = TransactionState.OPEN_show
    DIRECTION:dict = TransactionDirection.direction_read


@dataclass
class WriteTransaction(DbEntity):
    primary_key:int
    platform_id:int
    parity_id:int
    date_of_entry:str
    long_short:int #ii 1 (true,long) 0 false
    rr:float
    size:float
