from utils import common
from sqlalchemy import text

engine = common.db_handle()

def query(sql, **kwargs):
    con = engine.connect()
    if isinstance(sql, str):
        sql = text(sql)
    results = con.execute(sql, **kwargs)
    
    if results.cursor == None:
        return []
    
    data = [dict(zip(result.keys(), result)) for result in results]
    con.close()
    return data

def last_insert_id():
    '''
    get auto_increment id
    '''
    con = engine.connect()
    sql = text('SELECT LAST_INSERT_ID() as LastInsertedId')
    result = con.execute(sql).fetchone()
    con.close()
    return getattr(result,'LastInsertedId')
