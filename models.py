import sqlite3
from utils import key_by_uername

db_file = "data.db"

class Schema:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
        try:
            self.conn.execute("PRAGMA foreign_keys = ON")
        except:
            raise Exception("Cant turn 'foreign_keys' to 'ON'!")
        finally:
            self.create_table()
    
    def create_table(self):
        querys = [
            """
                CREATE TABLE IF NOT EXISTS user_league_of_legends (
                    user_key INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    region TEXT NOT NULL,
                    position0 TEXT,
                    position0_champion0 TEXT,
                    position0_champion1 TEXT,
                    position0_champion2 TEXT,
                    position1 TEXT,
                    position1_champion0 TEXT,
                    position1_champion1 TEXT,
                    position1_champion2 TEXT,
                    FOREIGN KEY (user_key) REFERENCES user (user_key)                   
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user_valorant (
                    user_key TEXT NOT NULL,
                    username TEXT NOT NULL,
                    region TEXT NOT NULL,
                    position0 TEXT,
                    position0_agent0 TEXT,
                    position0_agent1 TEXT,
                    position0_agent2 TEXT,
                    position1 TEXT,
                    position1_agent0 TEXT,
                    position1_agent1 TEXT,
                    position1_agent2 TEXT,
                    FOREIGN KEY (user_key) REFERENCES user (user_key)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS guild (
                    guild_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team (
                    team_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    game TEXT NOT NULL,
                    guild_key TEXT, 
                    FOREIGN KEY (guild_key) REFERENCES guild (guild_key)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team_discord (
                    team_key INTEGER NOT NULL,
                    role_team_id TEXT,
                    role_player_id TEXT,
                    role_team_id TEXT,
                    role_coach_id TEXT,
                    category_id TEXT,
                    channel_team_roaster TEXT,
                    channel_team_chat TEXT,
                    channel_shogun_chat TEXT,
                    channel_team_voice TEXT,
                    FOREIGN KEY (team_key) REFERENCES team (team_key)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user (
                    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    discord_id TEXT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user_team (
                    user_key INTEGER NOT NULL,
                    team_key INTEGER NOT NULL,
                    role TEXT,
                    FOREIGN KEY (user_key) REFERENCES user (user_key),
                    FOREIGN KEY (team_key) REFERENCES team (team_key) 
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user_guild (
                    user_key INTEGER NOT NULL,
                    guild_key INTEGER NOT NULL,
                    role TEXT,
                    FOREIGN KEY (user_key) REFERENCES user (user_key),
                    FOREIGN KEY (guild_key) REFERENCES guild (guild_key) 
                )
            """
        ]
        for query in querys:
            self.conn.execute(query)
            print(f'Creating table "{query.strip().split(' ')[5]}" successful.')


class UserModel:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
        
    def create(self,user_name:str,discord_id:str|None) -> str:
        query = f'INSERT INTO user (name) VALUES ("{user_name}")'
        if discord_id != None:
            query = f'INSERT INTO user (name, discord_id) VALUES ("{user_name}", "{discord_id}")'
        result = self.conn.execute(query)
        self.conn.commit()
        return f'Ok {result.lastrowid}'
    
    def get(self,user_name:str|None) -> list|dict|None:
        try: 
            cur = self.conn.cursor()
            result = []
            if user_name == None:
                cur.execute(f'SELECT * FROM user WHERE user_key = {user_name}')
            else:
                cur.execute('SELECT * FROM user')
            for elem in cur.fetchall():
                result.append({
                    "username": elem[1],
                    "discord_id": elem[2]
                })
            if len(result) == 1:
                result = result[0]
            return result
        except:
            return None
        
    def create_league_of_legends(self,user_name:str,ingame_name:str,region:str,position:list|None,discord_id:str|None) -> str:
        # create user if not exists
        if key_by_uername(self.conn,user_name) == None:
            self.create(user_name,discord_id)

        query = 'INSERT INTO user_league_of_legends (user_key, name, region'
        values = f'{key_by_uername(self.conn,user_name)}, "{ingame_name}", "{region}"'
        if position != None:
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
        return f'Ok {result.lastrowid}'
    
    def get_league_of_legends(self,user_name:str|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = []
            query = "SELECT * FROM user_league_of_legends "
            if user_name != None:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
            for acc in cur.fetchall():
                posititon = []
                pos = { "position": None, "champs": []}
                for i in range(len(acc)):
                    if i == 0:
                        pos = { "position": None, "champs": []}
                    if i == len(acc)-1 and pos["position"] != None:
                        posititon.append(pos)
                    if acc[i] != None:
                        if i == 3 or i == 7: 
                            pos["position"] = acc[i]
                        elif i > 3: 
                            pos["champs"].append(acc[i])
                this_acc = {
                    "ingame_name": acc[1],
                    "region": acc[2],
                    "position": posititon
                }
                if user_name == None:
                    cur.execute(f'SELECT * FROM user WHERE user_key = {acc[0]}')
                    this_acc["userna"] = cur.fetchall()[0][1]
                result.append(this_acc)
            return result
        except:
            return None
        
    def create_valorant(self,user_name:str,ingame_name:str,region:str,position:list|None,discord_id:str|None) -> str:  
        # create user if not exists
        if key_by_uername(self.conn,user_name) == None:
            self.create(user_name)

        query = 'INSERT INTO user_valorant (user_key, name, region'
        values = f'{key_by_uername(self.conn,user_name)}, "{ingame_name}", "{region}"'
        if position != None:
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
        return f'Ok {result.lastrowid}'

    def get_valorant(self,user_name:str|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = []
            query = "SELECT * FROM user_valorant "
            if user_name != None:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
            return result
        except:
            return None
        
class TeamModel:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
    
    def creat(self,name:str,member:list[int]) -> None:
        pass

    def get(self,name:str,member:list[int]) -> None:
        pass