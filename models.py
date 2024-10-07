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
            # user_league.main_acc, user_valorant.main_acc ( 1 = true / 0 = false )
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
    
    def search_or_create_user(self,user_name:str,discord_id:int) -> int|None:
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
            if discord_id != -1:
                self.conn.execute(f'INSERT INTO user (name, discord_id) VALUES ("{user_name}", "{discord_id}")')
            else:
                self.conn.execute(f'INSERT INTO user (name) VALUES ("{user_name}")')
            self.conn.commit()
            result = search()
        finally:
            return result
    
    def create_league(self,user_name:str,ingame_name:str,region:str,position:list[dict[str,list[str]]],discord_id=-1) -> str:
        query = 'INSERT INTO user_league_of_legends (user_key, name, region'
        values = f'{self.search_or_create_user(user_name,discord_id)}, "{ingame_name}", "{region}"'

        if len(position) > 0:
            query += ", "
            values += ", "
        for i in range(len(position)):
            query += f'position{i},'
            values += f'"{position[i].position}", '
            for j in range(len(position[i].champs)):
                query += f'position{i}_champion{j}'
                values += f'"{position[i].champs[j]}"'
                if i < range(len(position))-1 and j < len(position[i].champs)-1:
                    query += ', '
                    values += ', '
        query += f') VALUES ({values})'
        
        result = self.conn.execute(query)
        self.conn.commit()

        return f'Ok {result.lastrowid}'
    
Schema()

user = UserModel()
print(user.create_league("testUsername","testName#EUW","euw",[]))

# if main_acc == 0 or main_acc == 1:
#             if self.conn.execute()