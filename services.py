from models import UserLeagueModel

class UserLeagueService:
    def __init__(self) -> None:
        self.model = UserLeagueModel()

    def create(self, discord_id:str, summoner_name:str, region:str, position:list[dict[str,list[str]]])
        return self.model.create_league(discord_id, summoner_name, region, position)