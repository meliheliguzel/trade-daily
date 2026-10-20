class StrategyQuery:

    LOAD:str = "SELECT * from Strategy s ;"
    ADD:str = "insert into Strategy (name,description) VALUES (?,?);"
    UPDATE:str = "UPDATE Strategy SET name= ?,description = ? WHERE id == ? ;"
    REMOVE:str = "DELETE from Strategy where id = ?;"

    NAME_CONTROL:str = "SELECT count(*) from Strategy s WHERE s.name == ?;"
    NAME_CONTROL_UPDATE:str = "SELECT count(*) from Strategy s WHERE s.name == ? and s.id != ?;"
    DEL_CONTROL:str ="select COUNT(*) from Transaction_Strategy ts WHERE ts.strategy_id == ?;"
