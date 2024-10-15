import sqlite3, os, dotenv
from utils import UtilsModels

dotenv.load_dotenv() 

class User:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)

    def create(self,user_name:str,discord_id:str|None) -> str|None:
        try: 
            query = f'INSERT INTO user (name) VALUES ("{user_name}")'
            if discord_id:
                query = f'INSERT INTO user (name, discord_id) VALUES ("{user_name}", "{discord_id}")'
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except:
            return None
        
    def get(self,search:list|None) -> list|None:
        try: 
            cur = self.conn.cursor()
            query = "SELECT * FROM user "
            if search and len(search) == 2:
                query += f'WHERE {search[0]} = "{search[1]}"'
            cur.execute(query)
            result = []
            for elem in cur.fetchall():
                user = {"user_name": elem[1]}
                if elem[2]:
                    user["discord_id"] = elem[2]
                result.append(user)
            return result
        except:
            return None
        
class LeagueOfLegends:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)

    def create(self,user_name:str,ingame_name:str,position:list|None,discord_id:str|None) -> str|None:
        # create user if not exists
        if self.utils.key_by_name(user_name,"user") == None:
            User().create(user_name,discord_id)
        try:
            query = 'INSERT INTO user_league_of_legends (user_key, name '
            values = f'{self.utils.key_by_name(user_name,"user")}, "{ingame_name}"'
            if position:
                query += ", "
                values += ", "
                for i in range(len(position)):
                    query += f'position{i},'
                    values += f'"{position[i]["position"]}", '
                    for j in range(len(position[i]["champs"])):
                        query += f'position{i}_champion{j}'
                        values += f'"{position[i]["champs"][j]}"'
                        if not (i == len(position)-1 and j == len(position[i]["champs"])-1):
                            query += ', '
                            values += ', '
            query += f') VALUES ({values})'
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except:
            return None
        
    def get(self,search:list|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = {}
            user = User().get(search)
            for elem in user:
                cur.execute(f'SELECT * FROM user WHERE name = "{elem["user_name"]}"')
                cur.execute(f'SELECT * FROM user_league_of_legends WHERE user_key = {cur.fetchall()[0][0]}')
                accs = self.get_accs(cur.fetchall())
                result[elem["user_name"]] = { "user_name": elem["user_name"], "league_of_legends": accs }
                if "discord_id" in elem:
                    result[elem["user_name"]]["discord_id"] = elem["discord_id"]
            return result
        except: 
            return None
    
    def get_accs(self,accs:list) -> list:
        try: 
            cur = self.conn.cursor()
            result = []
            for acc in accs:
                posititon = []
                pos = { "position": None, "champs": []}
                for i in range(len(acc)):
                    if i == 0:
                        pos = { "position": None, "champs": []}
                    if i == len(acc)-1 and pos["position"]:
                        posititon.append(pos)
                    if acc[i]:
                        if i == 3 or i == 7: 
                            pos["position"] = acc[i]
                        elif i > 3: 
                            pos["champs"].append(acc[i])
                result.append({
                    "ingame_name": acc[1],
                    "position": posititon
                })
            return result
        except:
            return []

        
class Valorant:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)

    def create(self,user_name:str,ingame_name:str,position:list|None,discord_id:str|None) -> str|None:  
        # create user if not exists
        if self.utils.key_by_name(user_name,"user") == None:
            User().create(user_name,discord_id)
        try:
            query = 'INSERT INTO user_valorant (user_key, name'
            values = f'{self.utils.key_by_name(user_name,"user")}, "{ingame_name}"'
            # TODO: replace all with valorant logic
            if position:
                query += ", "
                values += ", "
                for i in range(len(position)):
                    query += f'position{i},'
                    values += f'"{position[i]["position"]}", '
                    for j in range(len(position[i]["champs"])):
                        query += f'position{i}_champion{j}'
                        values += f'"{position[i]["champs"][j]}"'
                        if not (i == len(position)-1 and j == len(position[i]["champs"])-1):
                            query += ', '
                            values += ', '
            query += f') VALUES ({values})'
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except:
            return None
        
    def get(self,user_name:str|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = []
            query = "SELECT * FROM user_valorant "
            if user_name:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            # TODO: add valorant logic
            cur.execute(query)
            return result
        except:
            return None


