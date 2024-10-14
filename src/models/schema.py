import sqlite3
import os, dotenv

dotenv.load_dotenv() 

class Schema:
    def __init__(self,db_file=os.getenv("DB_FILE")) -> None:
        self.conn = sqlite3.connect(str(db_file))
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
                    name TEXT NOT NULL UNIQUE,
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
                    name TEXT NOT NULL UNIQUE,
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
                    name TEXT UNIQUE,
                    description TEXT
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team (
                    team_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    game TEXT NOT NULL,
                    guild_key INTEGER, 
                    FOREIGN KEY (guild_key) REFERENCES guild (guild_key)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS team_discord (
                    team_key INTEGER NOT NULL,
                    server_id TEXt NOT NULL UNIQUE,
                    role_team_id TEXT UNIQUE,
                    role_player_id TEXT UNIQUE,
                    role_tryout_id TEXT UNIQUE,
                    role_coach_id TEXT UNIQUE,
                    category_id TEXT UNIQUE,
                    channel_team_roaster_id TEXT UNIQUE,
                    channel_team_chat_id TEXT UNIQUE,
                    channel_shogun_chat_id TEXT UNIQUE,
                    channel_team_voice_id TEXT UNIQUE,
                    FOREIGN KEY (team_key) REFERENCES team (team_key)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS user (
                    user_key INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    discord_id TEXT UNIQUE
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
