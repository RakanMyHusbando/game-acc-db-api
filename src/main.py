from flask import Flask, request
from models.schema import Schema
from utils import UtilsMain
import services.user as user 
import services.team as team
import services.guild as guild
import os, dotenv

dotenv.load_dotenv() 

utils = UtilsMain()
app = Flask(__name__)

@app.route("/api/user",methods = ["POST"])
def create():
    game = request.args.get("game")
    if not game:
        return user.User().create(request.get_json()), 201
    elif game == "league_of_legends":
        return user.LeagueOfLegends().create(request.get_json()), 201
    elif game == "valorant":
        return user.Valorant().create(request.get_json()), 201

@app.route("/api/user",methods = ["GET"])
def get():
    username = request.args.get("username")
    discord_id = request.args.get("discord_id")
    key = None
    value = None
    if username:
        key = "name"
        value = username
    elif discord_id:
        key = "discord_id"
        value = discord_id
    result = user.User().get(key,value)
    return utils.res_get(result)

@app.route("/api/user/<string:game>",methods = ["GET"])
def get_game_user(game:str):
    username = request.args.get("username")
    result = None
    if game == "league_of_legends":
        result = user.LeagueOfLegends().get(username)
    elif game == "valorant":
        result =  user.Valorant().get(username)
    return utils.res_get(result)


if __name__ == "__main__":
    Schema()
    app.run(
        debug=bool(os.getenv("DEBUG")),
        port=os.getenv("PORT")
    )
