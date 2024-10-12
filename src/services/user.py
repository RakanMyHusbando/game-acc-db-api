import models.user as model
from utils import UtilsServices 

utils = UtilsServices()

class User:
    def __init__(self) -> None:
        self.model = model.User()

    def create(self,input):
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"discord_id")
        )
    
    def get(self,*input):
        return self.model.get(
            input[0],
            input[1]
        )
    
class LeagueOfLegends:
    def __init__(self) -> None:
        self.model = model.LeagueOfLegends()

    def create(self,input) -> str:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"ingame_name"),
            utils.try_key(input,"region"),
            utils.try_key(input,"position"),
            utils.try_key(input,"discord_id")
        )
    
    def get(self,input) -> list:
        return self.model.get(input)
    
class Valorant:
    def __init__(self) -> None:
        self.model = model.Valorant()

    def create(self,input:dict) -> str:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"ingame_name"),
            utils.try_key(input,"region"),
            None,
            utils.try_key(input,"discord_id")
        )
    
    def get(self,input) -> list:
        return self.model.get(input)
    
class Team:
    def __init__(self) -> None:
        self.model = model.Team()

    def create(self,input) -> str:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"team_name"),
            utils.try_key(input,"role")
        )
    
    def get(self,input) -> list:
        pass