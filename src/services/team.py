import models.team as model
from utils import UtilsServices 

utils = UtilsServices()

class User:
    def __init__(self) -> None:
        self.model = model.User()

    def create(self,input) -> str|None:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"team_name"),
            utils.try_key(input,"role")
        )
    
    def get(self,input) -> list|None:
        return self.model.get(None,input)

class Team: 
    def __init__(self) -> None:
        self.model = model.Team()

    def create(self,input) -> str|None:
        
        return self.model.creat(
            utils.try_key(input,"team_name"),
            utils.try_key(input,"game"),
            utils.try_key(input,"guild_name"),
            utils.member_handle_json(input)
        )
    
    def get(self,input) -> list|None:
        return self.model.get(input)
    