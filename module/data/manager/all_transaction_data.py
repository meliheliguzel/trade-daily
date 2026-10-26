from config.query import DataDisplayQuery
from module.data.connection import Connect
from module.data.entities import (
    ChartImage,
    ChartLink,
    DbEntity,
    Note,
    Transaction,
    TransactionClosing,
    TransactionDetailClosing,
    TransactionDetailOpen,
    TransactionFullData,
    TransactionStrategy,
)

from .get_data import get_data


def all_transaction_data(
    connect: Connect, transaction_data: int | Transaction
) -> TransactionFullData:

    if type(transaction_data) == Transaction:
        transaction: Transaction = transaction_data
    elif type(transaction_data) == int:
        transaction: Transaction = get_data(
            connect,
            Transaction,
            DataDisplayQuery.TRANSACTION_ONE_LOAD,
            (transaction_data,),
        )[0]
    else:
        raise ValueError(
            "The transaction_data data type must be only Transaction or integer (Transaction.id)"
        )

    tprimary_key: tuple[int] = (transaction.primary_key,)

    chart_images: Exception | list[DbEntity] = get_data(
        connect, ChartImage, DataDisplayQuery.CHART_IMAGES, tprimary_key
    )
    chart_links: Exception | list[DbEntity] = get_data(
        connect, ChartLink, DataDisplayQuery.CHART_LINKS, tprimary_key
    )
    if not chart_links:
        chart_links = None
    if not chart_images:
        chart_images = None

    strategys: Exception | list[DbEntity] = get_data(
        connect, TransactionStrategy, DataDisplayQuery.STRATEGY, tprimary_key
    )
    if not strategys:
        strategys = None
    note: Exception | list[DbEntity] = get_data(connect, Note, DataDisplayQuery.NOTE, tprimary_key)
    if not note:
        note = None
    else:
        note = note[0]

    detail_open: Exception | list[DbEntity] = get_data(
        connect, TransactionDetailOpen, DataDisplayQuery.OPEN_DETAIL, tprimary_key
    )
    if not detail_open:
        detail_open = None
    else:

        detail_open = detail_open[0]

    if transaction.tp_sl is not None:
        closing: DbEntity = get_data(
            connect, TransactionClosing, DataDisplayQuery.CLOSING, tprimary_key
        )[0]
        detail_closing: Exception | list[DbEntity] = get_data(
            connect,
            TransactionDetailClosing,
            DataDisplayQuery.CLOSING_DETAIL,
            tprimary_key,
        )
        if not detail_closing:
            detail_closing = None
        else:
            detail_closing = detail_closing[0]
    else:
        closing = None
        detail_closing = None

    return TransactionFullData(
        transaction=transaction,
        strategy=strategys,
        note=note,
        chart_images=chart_images,
        chart_links=chart_links,
        detail_open=detail_open,
        closing=closing,
        detail_closing=detail_closing,
    )
