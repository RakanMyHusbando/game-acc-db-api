import models.team as model
from utils import UtilsServices 

utils = UtilsServices()


class Discord: 
    def __init__(self) -> None:
        self.model = model.Discord()

    def create(self,body) -> str|None:
        return self.model.create(
            utils.try_key(body,"team_name"),
            utils.try_key(body,"server"),
            utils.try_key(body,"category"),
            utils.try_key(body,"roles"),
            utils.try_key(body,"channels")
        )
    
    def get(self,search) -> list|None:
        return self.model.get(search)
    