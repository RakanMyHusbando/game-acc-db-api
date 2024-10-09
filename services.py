from models import UserModel
from utils import UtilsServices

class UserService:
    def __init__(self) -> None:
        self.model = UserModel()
        self.utils = UtilsServices()

    def create(self,input:dict) -> str:
        return self.model.create(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"discord_id")
        )

    def get(self,input:str|None) -> str:
        return self.model.get(input)
        
    def create_league_of_legends(self,input:dict) -> str:
        return self.model.create_league_of_legends(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"ingame_name"),
            self.utils.try_key(input,"region"),
            self.utils.try_key(input,"position"),
            self.utils.try_key(input,"discord_id")
        )
    
    def get_league_of_legends(self,input:str|None) -> list[dict]:
        return self.model.get_league_of_legends(input)
    
    def create_valorant(self,input:dict) -> str:
        return self.model.create_league_of_legends(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"ingame_name"),
            self.utils.try_key(input,"region"),
            None,
            self.utils.try_key(input,"discord_id")
        )
    
    def get_valorant(self,input:str|None) -> list[dict]:
        return self.model.get_league_of_legends(input)