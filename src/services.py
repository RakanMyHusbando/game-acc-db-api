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

    def get(self,search,props) -> list|None:
        result = self.model.Team().get(search)
        if props == None:
            return utils.res_get(result)
        name_i = {}
        for i in range(len(result)):
            name_i[result[i]["name"]] = i
        for prop in props:
            for name in name_i: 
                match prop:
                    case "discord":
                        result = utils.prop_in_user(
                            prop,
                            self.model.Discord().get(search),
                            name_i[name],
                            result
                        )
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
            case "league_of_legends":
                result = self.model.LeagueOfLegends().create(
                    utils.try_key(body,"user_name"),
                    utils.try_key(body,"ingame_name"),
                    utils.try_key(body,"position"),
                    utils.try_key(body,"discord_id")
                )
        return utils.res_post(result)
    
    def get(self,search,props) -> list|None:
        result = self.model.User().get(search)
        if props == None:
            return utils.res_get(result)
        name_i = {}
        for i in range(len(result)):
            name_i[result[i]["user_name"]] = i
        for prop in props:
            for name in name_i: 
                match prop:
                    case "league_of_legends":
                        result = utils.prop_in_user(
                            prop,
                            self.model.LeagueOfLegends().get(search),
                            name_i[name],
                            result
                        )
        return utils.res_get(result)