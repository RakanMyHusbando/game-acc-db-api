from models import UserModel, TeamModel
from utils import UtilsServices

class UserServices:
    def __init__(self) -> None:
        self.model = UserModel()
        self.utils = UtilsServices()

    def create(self,input:dict):
        return self.model.create(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"discord_id")
        )

    def get(self,*input):
        return self.model.get(
            input[0],
            input[1]
        )
        
    def create_league_of_legends(self,input):
        return self.model.create_league_of_legends(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"ingame_name"),
            self.utils.try_key(input,"region"),
            self.utils.try_key(input,"position"),
            self.utils.try_key(input,"discord_id")
        )
    
    def get_league_of_legends(self,input):
        return self.model.get_league_of_legends(input)
    
    def create_valorant(self,input:dict):
        return self.model.create_league_of_legends(
            self.utils.try_key(input,"user_name"),
            self.utils.try_key(input,"ingame_name"),
            self.utils.try_key(input,"region"),
            None,
            self.utils.try_key(input,"discord_id")
        )
    
    def get_valorant(self,input) -> list:
        return self.model.get_league_of_legends(input)
    
class TeamServices:
    def __init__(self,input) -> None:
        self.model = TeamModel()
        self.utils = UtilsServices()

    def create(self,input):
        pass
    
    def get(self,input) -> list:
        pass

    def create_user(self,input):
        pass
    
    def get_user(self,input) -> list:
        pass