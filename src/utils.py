from sqlite3 import Connection
from flask import jsonify

class UtilsServices:
    def try_key(self,input,*keys):
        try:
            result = input
            for elem in keys:
                result = result[elem]
            return result
        except:
            return None
    
class UtilsModels: 
    def __init__(self,conn:Connection) -> None:
        self.conn = conn

    def key_by_name(self,name:str,table:str):
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELECT {table}_key FROM {table} WHERE name = "{name}"')
            return cur.fetchall()[0][0]
        except:
            return None 

class UtilsMain:        
    def res_get(self,data):
        result = { "data": data, "status": 404 }
        if data != None:
            result["status"] = 200
        return jsonify(result), result["status"]
