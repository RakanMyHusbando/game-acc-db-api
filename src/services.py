import models.team as team
import models.user as user
from utils import UtilsServices 

utils = UtilsServices()

class Team: 
    def __init__(self) -> None:
        self.model = model_team()

    def create(self,body) -> str|None:
        return self.model.create(
            utils.try_key(body,"team_name"),
            utils.try_key(body,"game"),
            utils.try_key(body,"guild_name"),
            utils.member_handle_json(body)
        )
    
    def get(self,search,props) -> list|None:
        result = self.model.get(search)
        for prop in props:
            pass
    
class User:
    def __init__(self) -> None:
        self.user = user.User()
        self.league_of_legends = user.LeagueOfLegends()
        self.valorant = user.Valorant()

    def create(self,body) -> str|None:
        return self.model.create(
            utils.try_key(body,"user_name"),
            utils.try_key(body,"team_name"),
            utils.try_key(body,"role")
        )
    
    def get(self,search,props) -> list|None:
        result = self.user.get(search)
        name_i = {}
        for i in range(len(result)):
            name_i[result[i]["name"]] = i
        for prop in props:
            for name in name_i: 
                result_p = None
                match prop:
                    case "league_of_legends":
                        result_p = self.league_of_legends.get(search) 
                    case "valorant":
                        result_p = self.valorant.get(search)
                if result_p:
                    result[name] = result_p
        
        