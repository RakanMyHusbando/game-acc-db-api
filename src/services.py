from utils import UtilsServices 
from models.team import Team as model_team
from models.user import User as model_user
import properties.team as prop_team
import properties.user as prop_user

utils = UtilsServices()

class Team: 
    def __init__(self) -> None:
        self.team = model_team()
        self.discord = prop_team.Discord()

    def create(self,body,create) -> str|None:
        result = None
        match create:
            case None:
                result = self.team.create(
                    utils.try_key(body,"team_name"),
                    utils.try_key(body,"game"),
                    utils.try_key(body,"guild_name"),
                    utils.member_handle_json(body)
                )
            case "user":
                pass
            case "discord":
                self.discord.create(body)
        return utils.res_post(result)

    def get(self,search,props=[]) -> list|None:
        result = self.team.get(search)
        name_i = {}
        for i in range(len(result)):
            name_i[result[i]["name"]] = i
        for prop in props:
            for name in name_i: 
                result_p = None
                match prop:
                    case "discord":
                        result_p = self.discord.get(search) 
                if result_p:
                    result[name] = result_p

class User:
    def __init__(self) -> None:
        self.user = model_user()
        self.league_of_legends = prop_user.LeagueOfLegends()
        self.valorant = prop_user.Valorant()
        
    def create(self,body,create) -> str|None:
        result = None
        match create:
            case "league_of_leagends":
                pass
            case "valorant":
                pass
        if result == None:
            result = self.user.create(
                utils.try_key(body,"user_name"),
                utils.try_key(body,"discord_id")
            )
        return result
    
    def get(self,search,props=[]) -> list|None:
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