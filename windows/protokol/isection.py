from typing import Protocol

from module.utils import ThreadWorker

from .main import MainWindowProtocol


class ISectionProtokol(Protocol):

    def __init__(self,name:str):
        self._base:MainWindowProtocol
        self._thread_work:ThreadWorker
        self._therad_work:ThreadWorker
        self.__name:str

