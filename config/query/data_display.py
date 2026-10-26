from ..state_info_table import StateInfoTableRowConfig


class DataDisplayQuery:
    TRANSACTION_TABLE_MAIN: str = """
    SELECT
        t.id ,
        p2.name,
        p.name ,
        t.date_of_entry,
        t.long_short,
        t.rr ,
        t."size" ,
        tc.tp_sl
    FROM
        "Transaction" t
    LEFT JOIN
        Transaction_Closing tc ON t.id = tc.transaction_id
    LEFT  JOIN Parity p  ON t.parity_id  = p.id
    LEFT  JOIN Platform p2 ON t.platform_id = p2.id
    """
    LOAD: str = f"{TRANSACTION_TABLE_MAIN};"
    INSERT_ID: str = 'SELECT t.id from "Transaction" t ORDER BY t.id DESC LIMIT 1;'
    TRANSACTION_ONE_LOAD:str = f"{TRANSACTION_TABLE_MAIN} WHERE t.id == (?);"

    CHART_IMAGES: str = "SELECT * from Chart_Image ci where ci.transaction_id == (?);"
    CHART_LINKS: str = "SELECT * from Chart_Link cl where cl.transaction_id == (?);"
    STRATEGY: str = """
    SELECT ts.id ,ts.transaction_id, s.id, s.name from Transaction_Strategy ts
    left join Strategy s on ts.strategy_id = s.id
    where ts.transaction_id == (?);
    """
    NOTE: str = "SELECT * from Note n where n.transaction_id == (?);"
    CLOSING: str = (
        "SELECT * from Transaction_Closing tc where tc.transaction_id == (?);"
    )
    CLOSING_DETAIL: str = (
        "SELECT * from Transaction_Detail_Closing tdc where tdc.transaction_id == (?);"
    )
    OPEN_DETAIL: str = (
        "SELECT * from Transaction_Detail_Open tdo where tdo.transaction_id == (?);"
    )

    DATA_STATE_COUNT_TOTAL: str = 'SELECT count(*) from "Transaction" t ;'
    DATA_STATE_COUNT_SHORT: str = (
        'SELECT count(*) from "Transaction" t WHERE  t.long_short == 0;'
    )
    DATA_STATE_COUNT_LONG: str = (
        'SELECT count(*) from "Transaction" t WHERE  t.long_short == 1;'
    )
    DATA_STATE_COUNT_TP: str = (
        "SELECT count(*) from Transaction_Closing tc where tc.tp_sl == 1;"
    )
    DATA_STATE_COUNT_SL: str = (
        "SELECT count(*) from Transaction_Closing tc where tc.tp_sl == 0;"
    )
    DATA_STATE_COUNT_OPEN: str = """
    SELECT COUNT(*)
    FROM "Transaction" t
    LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
    WHERE tc.transaction_id IS NULL;"""

    STATE_LOAD: dict = {
        StateInfoTableRowConfig.OPEN: f"""{TRANSACTION_TABLE_MAIN} where t.id in
    (SELECT t.id
    FROM "Transaction" t
    LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
    WHERE tc.transaction_id IS NULL);""",
        StateInfoTableRowConfig.TP: f"""{TRANSACTION_TABLE_MAIN} where t.id in
    (SELECT t.id
    FROM "Transaction" t
    LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
    WHERE tc.tp_sl == 1);""",
        StateInfoTableRowConfig.SL: f"""{TRANSACTION_TABLE_MAIN} where t.id in
    (SELECT t.id
    FROM "Transaction" t
    LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
    WHERE tc.tp_sl == 0);""",
        StateInfoTableRowConfig.TOTAL: LOAD,
        StateInfoTableRowConfig.SHORT: f"""{TRANSACTION_TABLE_MAIN} where t.long_short == 0;""",
        StateInfoTableRowConfig.LONG: f"""{TRANSACTION_TABLE_MAIN} where t.long_short == 1 ;""",
    }
