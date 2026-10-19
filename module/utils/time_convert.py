from PySide6.QtCore import QDateTime
import datetime

def str_to_qDateTime(time:str) -> QDateTime:
    format: list[str] = ["d/M/yyyy HH:mm","d.M.yyyy HH:mm"]
    for i in format:
        dt: QDateTime = QDateTime.fromString(time, i)
        if dt.isValid():
            return dt
        
def current_time()-> QDateTime:
    
    now: datetime = datetime.datetime.now()
    return QDateTime(now.year,now.month,now.day,now.hour,now.minute,0)
