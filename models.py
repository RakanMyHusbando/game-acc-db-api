import sqlite3

db_file = "data.db"

class Schema:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
        self.create_table()
    
    def create_table(self):
        querys = [
            """
                CREATE TABLE IF NOT EXIST "user_league" (
                    discord_id TEXT,
                    summoner_name TEXT,
                    region TEXT,
                    position0 TEXT,
                    position0_champion0 TEXT,
                    position0_champion1 TEXT,
                    position0_champion2 TEXT,
                    position1 TEXT,
                    position1_champion0 TEXT,
                    position1_champion1 TEXT,
                    position1_champion2 TEXT
                )
            """
        ]
        for query in querys:
            self.conn.execute(query)

class UserModel:
    def __init__(self,db_file=db_file) -> None:
        self.conn = sqlite3.connect(db_file)
    
    def create_league(self,discord_id:str,summoner_name:str,region:str,position:list[dict[str,list[str]]]):
        query = 'insert into user_league (discord_id, summoner_name, region, '
        values = f'"{discord_id}", "{summoner_name}", "{region}", '

        for i in range(len(position)):
            query += f'position{i},'
            values += f'"{position[i].position}", '
            for j in range(len(position[i].champs)):
                query += f'position{i}_champion{j}'
                values += f'"{position[i].champs[j]}"'
                if i < range(len(position))-1 and j < len(position[i].champs)-1:
                    query += ', '
                    values += ', '
        query += f') values ({values})'

        result = self.conn.execute(query)
        self.conn.commit()

        return f'Ok {result.lastrowid}'