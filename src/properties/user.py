import models.user as model
from utils import UtilsServices 

utils = UtilsServices()

    
class LeagueOfLegends:
    def __init__(self) -> None:
        self.model = model.LeagueOfLegends()

    def create(self,input) -> str:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"ingame_name"),
            utils.try_key(input,"position"),
            utils.try_key(input,"discord_id")
        )
    
    def get(self,input) -> list|None:
        return self.model.get(input)
    
class Valorant:
    def __init__(self) -> None:
        self.model = model.Valorant()

    def create(self):
        pass
    
    def get(self):
        return
