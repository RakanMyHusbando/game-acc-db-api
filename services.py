from models import UserModel
from utils import try_key

class UserService:
    def __init__(self) -> None:
        self.model = UserModel()

    def create(self,input:dict) -> str:
        return self.model.create(
            try_key(input,"user_name"),
            try_key(input,"discord_id")
        )

    def get(self,input:dict) -> str:
        return self.model.get(
            try_key(input,"user_name"),
            try_key(input,"discord_id")
        )
        
    def create_league_of_legends(self,input:dict) -> str:
        return self.model.create_league_of_legends(
            try_key(input,"user_name"),
            try_key(input,"ingame_name"),
            try_key(input,"region"),
            try_key(input,"position"),
            try_key(input,"discord_id")
        )
    
    def get_league_of_legends(self,input:str|None) -> list[dict]:
        return self.model.get_league_of_legends(input)