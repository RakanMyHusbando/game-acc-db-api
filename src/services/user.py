import models.user as model
from utils import UtilsServices 

utils = UtilsServices()

class User:
    def __init__(self) -> None:
        self.model = model.User()

    def create(self,input) -> str|None:
        return self.model.create(
            utils.try_key(input,"user_name"),
            utils.try_key(input,"discord_id")
        )
    
    def get(self,input) -> list|None:
        try: 
            search = None
            games = []
            game_accs = {}
            result = []
            for key in input:
                if key == "game":
                    games = list(input[key])
                elif search == None:
                    search = [key,input[key]]
            for game in games:
                accs = {}
                match game:
                    case "league_of_legends":
                        accs = LeagueOfLegends().get(search)
                    case "valorant":
                        pass # TODO: add valorant
                for key in accs:
                    if key in accs:
                        game_accs[key] = accs[key]
                    else:
                        game_accs[key][game] = accs[key][game]
            if game_accs == {}:
                result = self.model.get(search)
            else:
                for key in game_accs:
                    result.append(game_accs[key])
            return result
        except:
            return None
    
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

    def create(self,input) -> str|None:
        pass
    
    def get(self,input) -> list|None:
        return
