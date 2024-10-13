import models.team as model
from utils import UtilsServices 

utils = UtilsServices()

class Team: 
    def __init__(self) -> None:
        self.model = model.Team()

    def create(self,input) -> str|None:
        member = None
        if utils.try_key(input,"member"):   
            member = [] 
            for key in input["member"]:
                if key == "main":
                    for role in input["member"][key]:
                        member.append([
                            input["member"][key][role],
                            f'main_{role}'
                        ])
                if key == "substitute":
                    for elem in input["member"][key]:
                        member.append([
                            elem["name"],
                            f'substitute_{elem["role"]}'
                        ])
                elif type(input["member"][key]) == str:
                    member.append([input["member"][key],key])
        return self.model.creat(
            utils.try_key(input,"team_name"),
            utils.try_key(input,"game"),
            utils.try_key(input,"guild_name"),
            member
        )
    
    def get(self,input) -> list|None:
        return self.model.get(input)
    