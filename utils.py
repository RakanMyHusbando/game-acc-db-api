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
    def key_by_uername(self,conn:Connection,user_name:str) -> int|None:
        cur = conn.cursor()
        try:
            cur.execute(f'SELECT user_key FROM user WHERE name = "{user_name}"')
            return cur.fetchall()[0][0]
        except:
            return None 

class UtilsMain:        
    def res_get(self,data):
        result = { "data": data, "status": 404 }
        if data != None:
            result["status"] = 200
        return jsonify(result), result["status"]
