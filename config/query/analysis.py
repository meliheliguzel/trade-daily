class AnalysisQuery:

    LONG_SHORT_COUNT: str = """
    SELECT long_short , COUNT(*)
    FROM "Transaction"
    GROUP BY long_short;
    """
    OPEN_COUNT: str = """
    SELECT COUNT(*)
    FROM "Transaction" t
    LEFT JOIN Transaction_Closing tc  ON t.id = tc.transaction_id
    WHERE tc.transaction_id IS NULL;
    """
    TP_SL_COUNT: str = """
    SELECT tc.tp_sl , COUNT(*)
    FROM Transaction_Closing tc
    GROUP BY tc.tp_sl;
    """
    STRATEGY_COUNT: str = """
    SELECT s.name , COUNT(*)
    FROM Transaction_Strategy ts
    left join Strategy s on ts.strategy_id == s.id
    GROUP BY ts.strategy_id;
    """
    PLATFORM_COUNT: str = """
    SELECT p.name , COUNT(*)
    FROM "Transaction" t
    left join Platform p  on t.platform_id  == p.id
    GROUP BY t.platform_id;"""
    RESULT: str = """
    SELECT tc.transaction_id ,tc."result"
    FROM Transaction_Closing tc ;
    """
    RR: str = """
    SELECT id ,rr
    FROM "Transaction";
    """
