import models.team as model
from utils import UtilsServices 

utils = UtilsServices()




    
class Discord: 
    def __init__(self) -> None:
        self.model = model.Discord()

    def create(self,input) -> str|None:
        return self.model.create(
            utils.try_key(input,"team_name"),
            utils.try_key(input,"server"),
            utils.try_key(input,"category"),
            utils.try_key(input,"roles"),
            utils.try_key(input,"channels")
        )
    
    def get(self,input) -> list|None:
        return self.model.get(input)
    