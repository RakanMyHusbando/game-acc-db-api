import sqlite3

def try_key(input,*keys):
    try:
        result = input
        for elem in keys:
            result = result[elem]
        return result
    except:
        return None

def key_by_uername(conn:sqlite3.Connection,user_name:str) -> int|None:
    cur = conn.cursor()
    try:
        cur.execute(f'SELECT user_key FROM user WHERE name = "{user_name}"')
        return cur.fetchall()[0][0]
    except:
        return None 