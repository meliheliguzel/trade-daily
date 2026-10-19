import pytest
from module.utils.singleton_meta import SingletonMeta


class DummySingleton(metaclass=SingletonMeta):
    def __init__(self, value=None):
        self.value = value


class AnotherDummySingleton(metaclass=SingletonMeta):
    def __init__(self, value=None):
        self.value = value


def test_singleton_same_instance():
    DummySingleton.reset()
    s1 = DummySingleton("first")
    s2 = DummySingleton("second")
    assert s1 is s2
    assert s1.value == "first"
    assert s2.value == "first"


def test_singleton_reset():
    DummySingleton.reset()
    s1 = DummySingleton("first")
    DummySingleton.reset()
    s2 = DummySingleton("second")
    assert s1 is not s2
    assert s1.value == "first"
    assert s2.value == "second"


def test_independent_subclasses():
    DummySingleton.reset()
    AnotherDummySingleton.reset()

    s1 = DummySingleton("A")
    s2 = AnotherDummySingleton("B")

    assert s1 is not s2
    assert isinstance(s1, DummySingleton)
    assert isinstance(s2, AnotherDummySingleton)
    assert s1.value == "A"
    assert s2.value == "B"
