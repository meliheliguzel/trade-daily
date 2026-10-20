class ParityQuery:

    LOAD:str = "SELECT * from Parity p WHERE p.platform_id == (?);"

    ADD:str = "insert into Parity (name,platform_id) VALUES (?,?);"
    UPDATE:str = "UPDATE Parity SET name=? ,platform_id=?  WHERE id == ? ;"
    REMOVE:str = "DELETE from Parity  where id = ?;"

    NAME_CONTROL:str = "SELECT count(*) from Parity p  WHERE p.name == ? and p.platform_id == ?;"
    NAME_CONTROL_UPDATE:str = "SELECT count(*) from Parity p WHERE p.name == ? and p.platform_id == ? and p.id != ?;"
    DEL_CONTROL:str ="select COUNT(*) from \"Transaction\" t WHERE t.parity_id == ?;"
