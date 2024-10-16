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
def user_create():
    game = request.args.get("game")
    match game:
        case None:
            return user.User().create(request.get_json())
        case "league_of_legends":
            return user.LeagueOfLegends().create(request.get_json())
        case "valorant":
            pass

@app.route("/api/user",methods = ["GET"])
def user_get():
    username = request.args.get("username")
    discord_id = request.args.get("discord_id")
    game = request.args.get("game")
    params = {}
    if username:
        params["name"] = username
    elif discord_id:
        params["discord_id"] = discord_id
    if game:
        params["game"] = game.split(",")
    return utils.res_get(
        user.User().get(params)
    )

########
# TEAM #
########

@app.route("/api/team",methods = ["POST"])
def team_create():
    prop = request.args.get("property")
    if prop: 
        for elem in prop.split(","):
            match elem:
                case "user":
                    return team.User().create(request.get_json())
                case "discord":
                    return team.Discord().create(request.get_json())
    else:
        return team.Team().create(request.get_json())

    

@app.route("/api/team",methods = ["GET"])
def team_get():
    teamname = request.args.get("teamname")
    username = request.args.get("username")
    prop = request.args.get("propery")
    search = None
    if teamname:
        search = ["team",teamname]
    elif username:
        search = ["user_team",username]
    result = team.Team().get(search)
    if prop:
        for elem in prop.split(","):
            match elem:
                case "discord": 
                    for i in range(len(result)):
                        team_discord = team.Discord().get(result[i]["name"])
                        if team_discord:
                            result[i]["discord"] = team_discord

if __name__ == "__main__":
    Schema()
    app.run(
        debug=bool(os.getenv("DEBUG")),
        port=int(os.getenv("PORT"))
    )
