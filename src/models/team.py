import sqlite3, os, dotenv
from utils import UtilsModels

dotenv.load_dotenv()

class User:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.getenv("DB_FILE"))
        self.utils = UtilsModels()
        
    def create(self,user_name:str,team_name:str,role:str) -> str|None:
        try:
            query = f'INSERT INTO user_team (user_key, team_key, role) VALUES ({self.utils.key_by_name(user_name,"user")},{self.utils.key_by_name(team_name,"team")},"{role}")'
            print(query)
            result = self.conn.execute(query)
            self.conn.commit()
            return f'ok {result.lastrowid}'
        except: 
            return None

    def get(self,search:list|None) -> dict|None:
        try: 
            cur = self.conn.cursor()
            query = "SELECT * FROM user_team "
            result = {}
            if search and search[0] == "team_name":
                team_key = self.utils.key_by_name(search[1],"team")
                query += f'WHERE team_key = {team_key}'
            cur.execute(query)
            for elem in cur.fetchall():
                player = {
                    "user_name": self.utils.name_where("user_key",elem[0],"user"),
                    "team_name": self.utils.name_where("team_key",elem[1],"team"),
                    "role": elem[2]
                }
                if search == None or search[0] != "user_name" or search[1] == player["user_name"]:
                    result[player["team_name"]] = player
            return result
        except:
            return None
        
class Team:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.getenv("DB_FILE"))
        self.utils = UtilsModels()
    
    def create(self,name:str,game:str,guild_name:str|None,member:list|None) -> str|None:
        try:
            query = "INSERT INTO team (name, game"
            values = f'"{name}", "{game}"'
            if guild_name:
                query += ", guild_key"
                values += f', "{self.utils.key_by_name(guild_name)}"'
            query += f') VALUES ({values})'
            result = self.conn.execute(query)
            self.conn.commit()
            if member:
                for elem in member:
                    User().create(elem[0],name,elem[1])
            return f'ok {result.lastrowid}'
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
                    print(member)
                    if member:
                        team_dict["member"] = member
                result.append(team_dict)
            return result
        except:
            return
        
    def league_of_legends_memeber(self,id:int) -> dict|None: 
        try:
            cur = self.conn.cursor()
            cur.execute(f'SELECT * FROM user_team WHERE team_key = {id}')
            roles = ["top","jng","mid","adc","sup"]
            member = {
                "main": {},
                "substitute": []
            }
            for user_team in cur.fetchall():
                cur.execute(f'SELECT name FROM user WHERE user_key = {user_team[0]}')
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
        
class Discord:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.getenv("DB_FILE"))
        self.utils = UtilsModels()

    def create(self,name:str,server_id:str,category_id:str|None,role_id:dict|None,channel_id:dict|None) -> str|None:
        try:
            team_key = self.utils.key_by_name(name,"team")
            if not team_key:
                raise Exception() #TODO
            query = "INSERT INTO team_discord (team_key, server_id"
            values = f'{team_key}, "{name}"'
            if server_id:
                query += ", server_id"
                values += f', {server_id}'
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
        
    def get(self,search:list|None) -> list|None:
        try:
            keys = [
                "team_key",
                "server_id",
                "role_team_id",
                "role_player_id",
                "role_tryout_id",
                "role_coach_id",
                "category_id",
                "channel_team_roaster_id",
                "channel_team_chat_id",
                "channel_shogun_chat_id",
                "channel_team_voice_id"
            ]
            cur = self.conn.cursor()
            query = "SELECT * FROM team_discord "
            result = []
            if search:
                cur.execute(f'SELECT team_key FROM team WHERE {search[0]} = "{search[1]}"')
                query += f'WHERE team_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
            teams = cur.fetchall()
            for team in teams:
                team_dict = { "role": {}, "channel": {} }
                for i in range(len(team)):
                    if team[i] and keys[i] != "team_key":
                        if team[i].split("_")[0] == "role" or team[i].split("_")[0] == "channel":
                            key = team[i].split("_")[0]
                            team_dict[key][team[i].replace(f"{key}_","")] = team[i]
                        else:
                            team_dict[keys[i]] = team[i]
                result.append(team_dict)
            return result
        except:
            return None