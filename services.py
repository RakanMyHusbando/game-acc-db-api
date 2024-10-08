from models import UserModel

def try_key(input,key):
    try:
        result = input[key]
        return result
    except Exception as err:
        print(err)
        return None

class UserService:
    def __init__(self) -> None:
        self.model = UserModel()
        
    def create_league_of_legends(self,input:dict) -> str:
        user_name = try_key(input,"user_name")
        ingame_name = try_key(input,"ingame_name")
        region = try_key(input,"region")
        position = try_key(input,"position")
        discord_id = try_key(input,"discord_id")

        if position == None:
            position = []
        if discord_id == None:
            discord_id = -1

        return self.model.create_user_league_of_legends(user_name,ingame_name,region,position,discord_id)
    
    def get_league_of_legends(self,input:str|None) -> list[dict]:
        return self.model.get_user_league_of_legends(input)