class BalanceQuery:

    SIZE_ADD: str = "insert into Balance_Size (size,state) VALUES (?,?);"
    SIZE_UPDATE: str = 'UPDATE Balance_Size set "size" = ?,state=? where id == ?;'

    ADD: str = (
        "insert into Balance (transaction_id,size_id,value,estimated) VALUES (?,?,?,?);"
    )

    DEL_BALANCE: str = "DELETE FROM Balance where size_id == ?;"
    SIZE_DEL: str = "DELETE FROM Balance_Size where id == ?;"

    LOAD: str = "SELECT * from Balance_Size;"

    LAST_ADDED: str = """
    SELECT * FROM Balance b
    WHERE b.size_id = 1
    ORDER BY id DESC
    LIMIT 1;
    """
    CALCULATE = """
    WITH param AS (
    SELECT ? AS "start_value", ? as "size_id"
    )
    SELECT id,param.size_id ,
    param.start_value + SUM(COALESCE("result", 0)) OVER ( ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as "result",
    param.start_value + SUM(estimated) OVER ( ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as "estimated"
    from (SELECT t.id,tc."result",
    CASE
        WHEN tc.tp_sl == 1
        THEN (t."size"*t.rr)
        WHEN tc.tp_sl == 0
        THEN -t."size"
        ELSE 0
        END AS "estimated"
    from "Transaction" t
    left join Transaction_Closing tc on t.id = tc.transaction_id),param;
    """

    SIZE_IDS: str = "SELECT id from Balance_Size;"
    BALANCE_GET: str = """
    select * from Balance b
    where b.size_id == ? ORDER BY b.transaction_id;"""
