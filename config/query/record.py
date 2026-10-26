class RecordQuery:

    OPEN_TRANSACTION: str = """
        SELECT t.id
        FROM "Transaction" t
        LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
        WHERE tc.transaction_id IS NULL;
        """

    INDEX_CONTROL: str = 'select COUNT(*) from "Transaction" t WHERE t.id  == ?;'

    CLOSING_CONTROL: str = (
        "select COUNT(*) from Transaction_Closing WHERE transaction_id == ?;"
    )
    NOTE_CONTROL: str = "select COUNT(*) from Note WHERE transaction_id == ?;"
    DETAIL_OPEN_CONTROL: str = (
        "select COUNT(*) from Transaction_Detail_Open WHERE transaction_id == ?;"
    )
    DETAIL_CLOSING_CONTROL: str = (
        "select COUNT(*) from Transaction_Detail_Closing WHERE transaction_id == ?;"
    )

    TRANSACTION_INSERT: str = """
    insert into "Transaction"
    (platform_id,parity_id,date_of_entry,long_short,rr,"size")
    VALUES (?,?,?,?,?,?);"""
    CLOSING_INSERT: str = """
    insert into Transaction_Closing
    (transaction_id,date_of_exit,tp_sl,"result") VALUES (?,?,?,?);"""
    NOTE_INSERT: str = "insert into Note  (transaction_id,note_text) VALUES (?,?);"
    DETAIL_OPEN_INSERT: str = """
    insert into Transaction_Detail_Open
    (transaction_id,enter_price,target_price,stop_price) VALUES (?,?,?,?);"""
    DETAIL_CLOSING_INSERT: str = """
    insert into Transaction_Detail_Closing
    (transaction_id,exit_price) VALUES (?,?);"""
    IMAGE_INSERT: str = """insert into Chart_Image (transaction_id,image,extension)
    VALUES (?,?,?);"""
    LINK_INSERT: str = "insert into Chart_Link (transaction_id,link) VALUES (?,?);"
    STRATEGY_INSERT: str = """
    insert into Transaction_Strategy
    (transaction_id,strategy_id) VALUES (?,?);"""

    TRANSACTION_UPDATE: str = """
    UPDATE "Transaction"
    SET platform_id=?,parity_id=?,date_of_entry=?,long_short=?,rr=?,"size"=?
    WHERE id == ? ;"""
    CLOSING_UPDATE: str = """
    UPDATE Transaction_Closing
    SET date_of_exit=?,tp_sl=?,"result"=? WHERE transaction_id == ? ;
    """
    NOTE_UPDATE: str = "UPDATE Note SET note_text=? WHERE transaction_id == ?;"
    DETAIL_OPEN_UPDATE: str = """
    UPDATE Transaction_Detail_Open
    SET enter_price=?,target_price=?,stop_price=? WHERE transaction_id == ? ;"""
    DETAIL_CLOSING_UPDATE: str = """
    UPDATE Transaction_Detail_Closing SET exit_price=? WHERE transaction_id == ? ;"""

    TRANSACTION_DELETE: str = 'DELETE from "Transaction" where id = ?;'
    CLOSING_DELETE: str = "DELETE from Transaction_Closing  where transaction_id = ?;"
    NOTE_DELETE: str = "DELETE from Note where transaction_id = ?;"
    DETAIL_OPEN_DELETE: str = (
        "DELETE from Transaction_Detail_Open where transaction_id = ?;"
    )
    DETAIL_CLOSING_DELETE: str = (
        "DELETE from Transaction_Detail_Closing where transaction_id = ?;"
    )

    IMAGE_DELETE_ALL: str = "DELETE from Chart_Image where transaction_id = ?;"
    IMAGE_DELETE_ONE: str = "DELETE from Chart_Image where id = ?;"
    LINK_DELETE_ALL: str = "DELETE from Chart_Link where transaction_id = ?;"
    LINK_DELETE_ONE: str = "DELETE from Chart_Link where id = ?;"
    STRATEGY_DELETE_ALL: str = (
        "DELETE from Transaction_Strategy where transaction_id = ?;"
    )
    STRATEGY_DELETE_ONE: str = "DELETE from Transaction_Strategy where id = ?;"
    BALANCE_DELTE: str = "DELETE FROM Balance where transaction_id == ?;"

