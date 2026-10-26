from module.utils import ThreadWorker
from scripts import ExceptState, except_work

from ..protokol.main import MainWindowProtocol


class ISection:

    def __init__(self, base: MainWindowProtocol):
        self._base: MainWindowProtocol = base
        self._thread_work: ThreadWorker = ThreadWorker()
        self._therad_work: ThreadWorker = self._thread_work
        self._thread_work.signals.error.connect(self.__show_error)

    @except_work(ExceptState.CRITICAL)
    def __show_error(self, e):
        raise Exception(e)


