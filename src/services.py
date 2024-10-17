from utils import UtilsServices 
from models import team, user, guild

utils = UtilsServices()

class Team: 
    def __init__(self) -> None:
        self.model = team

    def create(self,body,create) -> str|None:
        result = None
        match create:
            case None:
                result = self.model.Team().create(
                    utils.try_key(body,"team_name"),
                    utils.try_key(body,"game"),
                    utils.try_key(body,"guild_name"),
                    utils.member_handle_json(body)
                )
            case "user":
                result = self.model.User().create(
                    utils.try_key(body,"user_name"),
                    utils.try_key(body,"team_name"),
                    utils.try_key(body,"role")
                )
            case "discord":
                result = self.model.Discord().create(
                    utils.try_key(body,"team_name"),
                    utils.try_key(body,"server"),
                    utils.try_key(body,"category"),
                    utils.try_key(body,"roles"),
                    utils.try_key(body,"channels")
                )
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
        return utils.res_get(result)

class User:
    def __init__(self) -> None:
        self.model = user
        
    def create(self,body,create) -> str|None:
        result = None
        match create:
            case None:
                result = self.model.User().create(
                    utils.try_key(body,"user_name"),
                    utils.try_key(body,"discord_id")
                )
            case "league_of_leagends":
                result = self.model.LeagueOfLegends().create(
                    utils.try_key(body,"user_name"),
                    utils.try_key(body,"ingame_name"),
                    utils.try_key(body,"position"),
                    utils.try_key(body,"discord_id")
                )
        return utils.res_post(result)
    
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
        return utils.res_get(result)