from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .except_works import ExceptState, except_work
    from .table_load import daily_table_load, state_info_table_load

__all__ = [
    "ExceptState",
    "daily_table_load",
    "except_work",
    "state_info_table_load",
]


def __getattr__(name: str):
    if name in ("ExceptState", "except_work"):
        from . import except_works

        val = getattr(except_works, name)
        globals()[name] = val
        return val
    if name in ("daily_table_load", "state_info_table_load"):
        from . import table_load

        val = getattr(table_load, name)
        globals()[name] = val
        return val
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

