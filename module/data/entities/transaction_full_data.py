from dataclasses import dataclass

from .chart_image import ChartImage
from .chart_link import ChartLink
from .note import Note
from .transaction import Transaction
from .transaction_closing import TransactionClosing
from .transaction_detail_closing import TransactionDetailClosing
from .transaction_detail_open import TransactionDetailOpen
from .transaction_strategy import TransactionStrategy


@dataclass
class TransactionFullData:
    transaction:Transaction
    strategy:list[TransactionStrategy]|None
    note:Note|None
    chart_images:list[ChartImage]|None
    chart_links:list[ChartLink]|None
    detail_open:TransactionDetailOpen|None
    closing:TransactionClosing|None
    detail_closing:TransactionDetailClosing|None
