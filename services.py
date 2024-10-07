from models import UserModel

class UserLeagueOfLegendsService:
    def __init__(self) -> None:
        self.model = UserModel()

    def create(self,data:dict) -> str:
        def try_key(key):
            try:
                result = data[key]
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
    
    def get(self,user_name:str) -> list[dict]:
        return self.model.get_user_league_of_legends(user_name)