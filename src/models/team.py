import sqlite3, os, dotenv
from utils import UtilsModels

dotenv.load_dotenv() 

class User:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)
        
    def create(self,user_name:str,team_name:str,role:str) -> str|None:
        try:
            query = f'INSERT INTO user_team (user_key, team_key, role) VALUES ({self.utils.key_by_name(user_name,"user")},{self.utils.key_by_name(team_name,"team")},"{role}")'
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except: 
            return None

    def get(self,team_name:str|None,user_name:str|None) -> list|None:
        try: 
            cur = self.conn.cursor()
            query = "SELECT * FROM user_team "
            result = []
            if team_name:
                team_key = self.utils.key_by_name(team_name,"team")
                query += f'WHERE team_key = {team_key}'
            cur.execute(query)
            for elem in cur.fetchall():
                player = {
                    "user_name": self.utils.name_where("user_key",elem[0],"user"),
                    "team_name": self.utils.name_where("team_key",elem[1],"team"),
                    "role": elem[2]
                }
                if user_name == None or user_name == player["user_name"]:
                    result.append(player)
            return result
        except:
            return None
        
class Team:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)
    
    def creat(self,name:str,game:str,guild_name:str|None,member:list[list]|None) -> str|None:
        try:
            query = "INSERT INTO team (name, game"
            values = f'"{name}", "{game}"'
            if guild_name:
                query += ", guild_key"
                values += f', "{guild_name}"'
            query += f') VALUES ({values})'
            result_team = self.conn.execute(query)
            self.conn.commit()
            result_user = None
            if member:
                for elem in member:
                    result_user = User().create(elem[0],name,elem[1])
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
                    member = self.league_of_legends_memeber(team[0])
                    if member:
                        team_dict["member"] = member
                result.append(team_dict)
            return result
        except:
            return None
        
    def league_of_legends_memeber(self,id:int) -> dict|None: 
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
            return None
        
    def valorant_memeber(self,id:int) -> dict|None: 
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
        
class Discord:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(db_file)
        self.utils = UtilsModels(self.conn)

    def create(self,name:str,server_id:str,category_id:str|None,role_id:dict|None,channel_id:dict|None) -> str|None:
        try:
            team_key = self.utils.key_by_name(name,"team")
            if not team_key:
                raise Exception()
            query = "INSERT INTO team_discord (team_key, server_id"
            values = f'{team_key}, "{name}"'
            if category_id:
                query += ", category_id"
                values += f', {category_id}'
            if role_id:
                for key in role_id:
                    query += f', role_{key}_id'
                    values += f', {role_id[key]}'
            if channel_id:
                for key in channel_id:
                    query += f', channel_{key}_id'
                    values += f', {channel_id[key]}'
            query += f') VALUES ({values})'
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except:
            return None
        
    def get(self,name:str|None) -> list|None:
        pass
