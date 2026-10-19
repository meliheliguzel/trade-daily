from module.utils import ThreadWorker
import pytest
import time
from PySide6.QtCore import QCoreApplication, QEventLoop
from PySide6.QtTest import QSignalSpy

def sample_function(x):
    return x * 2

@pytest.fixture(scope="session")
def app():
    """Global QCoreApplication fixture."""
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QCoreApplication.instance() or QCoreApplication([])
    yield app

@pytest.fixture
def thread_worker():
    worker = ThreadWorker()
    yield worker
    worker.stop()
    worker.wait()

def test_add_work_starts_thread(thread_worker:ThreadWorker):
    assert not thread_worker.isRunning()
    thread_worker.add_work(sample_function, [2])
    assert thread_worker.isRunning()

def test_run_function_in_queue(app, thread_worker:ThreadWorker):
    #signal = Signal()
    spy = QSignalSpy(thread_worker.signals.finished)#signal
    thread_worker.add_work(sample_function, [2])
    while not spy.count():
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    assert spy.count() == 1

def test_pause_resume(app, thread_worker:ThreadWorker):
    spy = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(sample_function, [2])
    thread_worker.pause()
    QCoreApplication.processEvents(QEventLoop.AllEvents, 500)
    assert thread_worker.is_paused
    thread_worker.resume()
    while not spy.count():
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    assert spy.count() == 1

def test_stop_clears_queue(thread_worker:ThreadWorker):
    thread_worker.add_work(sample_function, [2])
    thread_worker.stop()
    thread_worker.wait()
    assert len(thread_worker.work_queue) == 0
    assert not thread_worker.isRunning()

def test_error_signal(app, thread_worker:ThreadWorker):
    
    def error_function():
        raise ValueError("Test error")

    spy_error = QSignalSpy(thread_worker.signals.error)
    thread_worker.add_work(error_function)
    while not spy_error.count():
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    assert spy_error.count() == 1
    assert "Error in function error_function: Test error" in spy_error.at(0)

def test_multiple_works(app, thread_worker:ThreadWorker):
    spy = QSignalSpy(thread_worker.signals.finished)
    num_tasks = 10
    for i in range(num_tasks):
        thread_worker.add_work(sample_function, [i])
    
    while spy.count() < num_tasks:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy.count() == num_tasks

def test_different_errors(app, thread_worker:ThreadWorker):
    def error_function_1():
        raise ValueError("Test error 1")
    
    def error_function_2():
        raise RuntimeError("Test error 2")

    spy_error = QSignalSpy(thread_worker.signals.error)
    thread_worker.add_work(error_function_1)
    thread_worker.add_work(error_function_2)

    while spy_error.count() < 2:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy_error.count() == 2
    assert "Error in function error_function_1: Test error 1" in spy_error.at(0)
    assert "Error in function error_function_2: Test error 2" in spy_error.at(1)

def test_pause_resume_combinations(app, thread_worker:ThreadWorker):
    spy = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(sample_function, [2])
    thread_worker.add_work(sample_function, [4])
    thread_worker.pause()
    QCoreApplication.processEvents(QEventLoop.AllEvents, 500)
    assert thread_worker.is_paused
    thread_worker.resume()
    
    while spy.count() < 2:
        thread_worker.pause()
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
        thread_worker.resume()
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy.count() == 2

def test_multiple_works_order(app, thread_worker:ThreadWorker):
    results = []
    def sample_function_with_result(x):
        results.append(x)

    num_tasks = 10
    for i in range(num_tasks):
        thread_worker.add_work(sample_function_with_result, [i])
    
    while len(results) < num_tasks:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert results == list(range(num_tasks))

def test_pause_add_work_resume(app, thread_worker:ThreadWorker):
    spy = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(sample_function, [2])
    thread_worker.pause()
    QCoreApplication.processEvents(QEventLoop.AllEvents, 500)
    thread_worker.add_work(sample_function, [4])
    thread_worker.resume()
    
    while spy.count() < 2:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy.count() == 2

def test_stop_when_queue_empty(thread_worker:ThreadWorker):
    thread_worker.stop()
    assert not thread_worker.isRunning()
    assert len(thread_worker.work_queue) == 0
    assert thread_worker.is_paused

def test_error_and_successful_functions(app, thread_worker:ThreadWorker):
    def error_function():
        raise ValueError("Test error")

    spy_error = QSignalSpy(thread_worker.signals.error)
    spy_finished = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(error_function)
    thread_worker.add_work(sample_function, [2])

    while spy_error.count() < 1 or spy_finished.count() < 1:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy_error.count() == 1
    assert spy_finished.count() == 1
    assert "Error in function error_function: Test error" in spy_error.at(0)


def test_slow_function(app, thread_worker:ThreadWorker):
    def slow_function():
        time.sleep(1)  # Sleep to simulate slow function
        return "Done"

    spy = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(slow_function)
    
    while not spy.count():
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy.count() == 1

def test_full_queue(app, thread_worker:ThreadWorker):
    results = []
    def sample_function_with_result(x):
        results.append(x)

    max_tasks = 100  # Enqueue multiple tasks
    for i in range(max_tasks):
        thread_worker.add_work(sample_function_with_result, [i])
    
    while len(results) < max_tasks:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert len(results) == max_tasks

def test_pause_resume_stop_combinations(app, thread_worker:ThreadWorker):
    def slow_function():
        time.sleep(0.5)
    spy = QSignalSpy(thread_worker.signals.finished)
    thread_worker.add_work(sample_function, [2])
    thread_worker.add_work(slow_function)
    thread_worker.pause()
    QCoreApplication.processEvents(QEventLoop.AllEvents, 500)
    assert thread_worker.is_paused
    thread_worker.resume()
    
    while spy.count() < 1:
        thread_worker.pause()
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
        thread_worker.resume()
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    thread_worker.stop()
    thread_worker.wait()
    assert spy.count() == 1  # Verify tasks did not continue after stop

def test_multiple_workers(app):
    worker1 = ThreadWorker()
    worker2 = ThreadWorker()
    spy1 = QSignalSpy(worker1.signals.finished)
    spy2 = QSignalSpy(worker2.signals.finished)

    worker1.add_work(sample_function, [2])
    worker2.add_work(sample_function, [3])
    
    while not spy1.count() or not spy2.count():
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)
    
    assert spy1.count() == 1
    assert spy2.count() == 1
    worker1.stop()
    worker2.stop()
    worker1.wait()
    worker2.wait()
