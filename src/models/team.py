import sqlite3, os, dotenv
from utils import UtilsModels
import user 

dotenv.load_dotenv() 

class Team:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
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
                result_user = user.Team().create(team[0],name,team[1])
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
                    team_dict["member"] = self.league_of_legends_memeber(team[0])
                elif team[2] == "valorant":
                    team_dict["member"] = self.valorant_memeber(team[0])
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
            return True
        
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

