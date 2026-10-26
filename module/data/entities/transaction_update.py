from dataclasses import dataclass

from .transaction_full_data import TransactionFullData


@dataclass
class TransactionUpdateData:

    ORIGINAL_DATA:TransactionFullData
    STRATEGY_REMOVE_IDS: list[int]
    CHART_IMAGE_REMOVE_IDS: list[int]
    CHART_LINK_REMOVE_IDS: list[int]





