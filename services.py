from models import UserModel

class UserLeagueOfLegendsService:
    def __init__(self) -> None:
        self.model = UserModel()

    def create(self,arg:dict) -> str:
        def try_key(key):
            try:
                result = arg[key]
                return result
            except Exception as err:
                print(err)
                return None
            
        user_name = try_key("user_name")
        ingame_name = try_key("ingame_name")
        region = try_key("region")
        position = try_key("position")
        discord_id = try_key("discord_id")

        if position == None:
            position = []
        if discord_id == None:
            discord_id = -1

        return self.model.create_user_league_of_legends(user_name,ingame_name,region,position,discord_id)
    
    def get(self,arg:str) -> list[dict]:
        name = arg
        if arg == "*":
            name = None
        return self.model.get_user_league_of_legends(name)