import sqlite3, os, dotenv
from utils import UtilsModels

dotenv.load_dotenv() 

db_file = os.getenv("DB_FILE")

class Schema:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
        try:
            self.conn.execute("PRAGMA foreign_keys = ON")
        except:
            raise Exception("Cant turn 'foreign_keys' to 'ON'!")
        finally:
            self.create_table()
    
    def create_table(self) -> None:
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
                    role_tryout_id TEXT,
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

    def get(self,search_by:str|None,value:str|None) -> list|None:
        try: 
            cur = self.conn.cursor()
            query = "SELECT * FROM user "
            if search_by and value:
                query += f'WHERE {search_by} = "{value}"'
            print(query)
            cur.execute(query)
            result = []
            for team in cur.fetchall():
                result.append({
                    "username": team[1],
                    "discord_id": team[2]
                })
            return result
        except:
            return None
        
    def create_league_of_legends(self,user_name:str,ingame_name:str,region:str,position:list|None,discord_id:str|None) -> str|None:
        # create user if not exists
        if self.utils.key_by_name(user_name,"user") == None:
            self.create(user_name,discord_id)
        try:
            query = 'INSERT INTO user_league_of_legends (user_key, name, region'
            values = f'{self.utils.key_by_name(user_name,"user")}, "{ingame_name}", "{region}"'
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
    
    def get_league_of_legends(self,user_name:str|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = []
            query = "SELECT * FROM user_league_of_legends "
            if user_name:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
            for acc in cur.fetchall():
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
        
    def create_valorant(self,user_name:str,ingame_name:str,region:str,position:list|None,discord_id:str|None) -> str|None:  
        # create user if not exists
        if self.utils.key_by_name(user_name,"user") == None:
            self.create(user_name,discord_id)
        try:
            query = 'INSERT INTO user_valorant (user_key, name, region'
            values = f'{self.utils.key_by_name(user_name,"user")}, "{ingame_name}", "{region}"'
            # TODO: replace all with a fitting script for valorant
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

    def get_valorant(self,user_name:str|None) -> list|None:  
        try:
            cur = self.conn.cursor()
            result = []
            query = "SELECT * FROM user_valorant "
            if user_name:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
            return result
        except:
            return None
        
class TeamModel:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)
    
    def creat(self,name:str,game:str,guild_name:str|None,*member:list) -> str|None:
        try:
            query = "INSERT INTO team (name, game"
            values = f'{name}, {game}'
            if guild_name:
                query += ", guild_key"
                values += f', {guild_name}'
            query += f') VALUES ({values})'
            result_team = self.conn.execute(query)
            self.conn.commit()
            result_user = None
            for team in member:
                result_user = self.create_user(team[0],name,team[1])
                self.conn.commit()
            if result_user:
                return  "team " + f'ok {result_team.lastrowid}', "user " + f'ok {result_user.lastrowid}'
            else:
                return f'ok {result_team.lastrowid}'
        except:
            return None

    def get(self,name:str|None) -> list|None:
        try:
            cur = self.conn.cursor()
            query = "SELECT * FROM team "
            result = []
            if name:
                query += f'WHERE name = "{name}"'
            cur.execute(query)
            for team in cur.fetchall():
                team_dict = {
                    "name": team[1],
                    "game": team[2],
                }
                if team[3]:
                    cur.execute(f'SELCT * FROM guild WHERE guild_key = {team[3]}')
                    team["guild"] = cur.fetchall()[1]
                if team[2] == "league_of_legends":
                    team_dict["member"] = self.get_league_of_legends_memeber(team[0])
                elif team[2] == "valorant":
                    team_dict["member"] = self.get_valorant_memeber(team[0])
                result.append(team_dict)
            return result
        except:
            return None
        
    def get_league_of_legends_memeber(self,id:int) -> dict|None: 
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELCT * FROM user_team WHERE team_key = {id}')
            roles = ["top","jng","mid","adc","sup"]
            member = {
                "main": {},
                "substitute": []
            }
            for user_team in cur.fetchall():
                cur.execute(f'SELCT name FROM user WHERE user_key = {user_team[0]}')
                username = cur.fetchall()[0][0]
                found = False
                for role in roles:
                    if "main_" + role == user_team[2]:
                        member["main"][role] = username 
                        found = True
                    if "substitute_" + role == user_team[2]:
                        member["substitute"].append({"role":role,"name":username})
                        found = True
                if found == False:
                    member[user_team[2]] = username 
            return member 
        except:
            return True
        
    def get_valorant_memeber(self,id:int) -> dict|None: 
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELCT * FROM user_team WHERE team_key = {id}')
            member = {
                "main": {},
                "substitute": []
            }
            for user_team in cur.fetchall():
                cur.execute(f'SELCT name FROM user WHERE user_key = {user_team[0]}')
                username = cur.fetchall()[0][0]
                found = False
                # TODO: add main and sub positions 
                if found == False:
                    member[user_team[2]] = username 
            return member 
        except:
            return True

    def create_user(self,user_name:str,team_name:str,role:str) -> str:
        try:
            query = f'''INSERT INTO team (user_key, team_key, role) VALUES ({
                self.utils.key_by_name(user_name,"user")
            }, {
                self.utils.key_by_name(team_name,"team")
            }, {
                role
            })'''
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except: 
            None

    def get_user(self,name:str,user_name:str) -> list|None:
        pass
