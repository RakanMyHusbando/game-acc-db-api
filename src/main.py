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

########
# USER #
########

@app.route("/api/user",methods = ["POST"])
def create():
    game = request.args.get("game")
    result = None
    if not game:
        result = user.User().create(request.get_json())
    elif game == "league_of_legends":
<<<<<<< HEAD
        return user.LeagueOfLegends().create(request.get_json()), 201
=======
        result = user.LeagueOfLegends().create(request.get_json())
>>>>>>> in-progress
    elif game == "valorant":
        result = user.Valorant().create(request.get_json())
    return utils.res_post(result)

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
    return utils.res_get(
        user.User().get(key,value)
    )

@app.route("/api/user/<string:game>",methods = ["GET"])
def get_game_user(game:str):
    username = request.args.get("username")
    result = None
    if game == "league_of_legends":
        result = user.LeagueOfLegends().get(username)
    elif game == "valorant":
        result =  user.Valorant().get(username)
    return utils.res_get(result)

########
# TEAM #
########

@app.route("/api/team",methods = ["POST"])
def create_team():
    return utils.res_post(
        team.Team().create(request.get_json())
    )

@app.route("/api/team",methods = ["GET"])
def get_team():
    teamname = request.args.get("teamname")
    return utils.res_get(
        team.Team().get(teamname)
    )

@app.route("/api/team/user",methods = ["POST"])
def create_user_team():
    return utils.res_post(
        team.User().create(request.get_json())
    )

@app.route("/api/team/user",methods = ["GET"])
def get_user_team():
    username = request.args.get("username")
    return utils.res_get(
        team.User().get(username)
    )

if __name__ == "__main__":
    Schema()
    app.run(
        debug=bool(os.getenv("DEBUG")),
<<<<<<< HEAD
        port=os.getenv("PORT")
=======
        port=int(os.getenv("PORT"))
>>>>>>> in-progress
    )
