import sqlite3
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
    def member_handle_json(self,input):
        member = None
        if self.try_key(input,"member"):   
            member = [] 
            for key in input["member"]:
                if key == "main":
                    for role in input["member"][key]:
                        member.append([
                            input["member"][key][role],
                            f'main_{role}'
                        ])
                if key == "substitute":
                    for elem in input["member"][key]:
                        member.append([
                            elem["name"],
                            f'substitute_{elem["role"]}'
                        ])
                elif type(input["member"][key]) == str:
                    member.append([input["member"][key],key])
        return member
    def res_get(self,data):
        result = { "data": data, "status": 404 }
        if data != None:
            result["status"] = 200
        return jsonify(result), result["status"]
    def res_post(self,response):
        result = { "response": response, "status": 404 }
        if response != None:
            result["status"] = 201
        return jsonify(result), result["status"]
    
class UtilsModels: 
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.getenv("DB_FILE"))

    def key_by_name(self,name:str,table:str):
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELECT {table}_key FROM {table} WHERE name = "{name}"')
            return cur.fetchall()[0][0]
        except:
            return None 
    def name_where(self,where_key:str,where_value:int,table:str):
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELECT name FROM {table} WHERE {where_key} = {where_value}')
            return cur.fetchall()[0][0]
        except:
            return None 
