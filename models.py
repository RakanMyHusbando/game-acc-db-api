import sqlite3

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
                    name BLOB NOT NULL,
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
                    username BLOB NOT NULL,
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
                    name BLOB,
                    description TEXT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team (
                    team_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name BLOB
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team_guild (
                    team_key INTEGER NOT NULL,
                    guild_key INTEGER NOT NULL,
                    FOREIGN KEY (team_key) REFERENCES team (team_key),
                    FOREIGN KEY (guild_key) REFERENCES guild (guild_key) 
                )        
            """,
            """
                CREATE TABLE IF NOT EXISTS user (
                    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name BLOB NOT NULL,
                    discord_id TEXT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user_team (
                    user_key INTEGER NOT NULL,
                    team_key INTEGER NOT NULL,
                    FOREIGN KEY (user_key) REFERENCES user (user_key),
                    FOREIGN KEY (team_key) REFERENCES team (team_key) 
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user_guild (
                    user_key INTEGER NOT NULL,
                    guild_key INTEGER NOT NULL,
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
    
    def search_or_create_user(self,user_name:str,discord_id:str|None) -> int|None:
        cur = self.conn.cursor()
        result = None

        def search():
            cur.execute(f'SELECT user_key FROM user WHERE name = "{user_name}"')
            return cur.fetchall()[0][0]
        
        try:
            result = search()
            if type(result) != int:
                raise Exception()
        except:
            query = f'INSERT INTO user (name) VALUES ("{user_name}")'
            if discord_id != None:
                query = f'INSERT INTO user (name, discord_id) VALUES ("{user_name}", "{discord_id}")'
            self.conn.execute(query)
            self.conn.commit()
            result = search()
        finally:
            return result
        
    # positiom = [ { position: str, champs:[str,str,str] }, ... ] -> max length 2
    def create_user_league_of_legends(self,user_name:str,ingame_name:str,region:str,position:list,discord_id:str|None) -> str:
        query = 'INSERT INTO user_league_of_legends (user_key, name, region'
        values = f'{self.search_or_create_user(user_name,discord_id)}, "{ingame_name}", "{region}"'
        print(position)
        if len(position) > 0:
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
    
    def get_user_league_of_legends(self,user_name:str|None) -> list|None:
        cur = self.conn.cursor()
        def create_acc_list(accs):
            result = []
            for acc in accs:
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
                result.append({
                    "ingame_name": acc[1],
                    "region": acc[2],
                    "position": posititon
                })
            return result
        try: 
            query = "SELECT * FROM user_league_of_legends "
            if user_name == None:
                cur.execute(f'SELECT * FROM user WHERE name = "{user_name}"')
                query += f'WHERE user_key = {cur.fetchall()[0][0]}'
            cur.execute(query)
        except:
            return None
        finally:
            return create_acc_list(cur.fetchall())
        
