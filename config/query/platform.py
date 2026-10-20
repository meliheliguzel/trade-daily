class PlatformQuery:

    LOAD:str = "SELECT * from Platform p ;"
    ADD:str = "insert into Platform (name) VALUES (?);"
    UPDATE:str = "UPDATE Platform  SET name= ? WHERE id == ?;"
    REMOVE:str = "DELETE from Platform  where id = ?;"

    NAME_CONTROL:str = "SELECT count(*) from Platform p  WHERE p.name == ?;"
    NAME_CONTROL_UPDATE:str = "SELECT count(*) from Platform p WHERE p.name == ? and p.id != ?;"
    DEL_CONTROL:str ="select COUNT(*) from  Parity p  WHERE  p.platform_id == ?;"
