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
        result = user.LeagueOfLegends().create(request.get_json())
    elif game == "valorant":
        result = user.Valorant().create(request.get_json())
    return utils.res_post(result)

@app.route("/api/user",methods = ["GET"])
def get():
    username = request.args.get("username")
    discord_id = request.args.get("discord_id")
    game = request.args.get("game")
    result = None
    query_param = ()
    if username:
        query_param.append(["name",username])
    elif discord_id:
        query_param.append(["discord_id",discord_id])
    if game:
        query_param.append(["game",game])


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

@app.route("/api/team/discord",methods = ["POST"])
def creat_team_discord():
    utils.res_post(
        team.Discord().create(request.get_json())
    )

if __name__ == "__main__":
    Schema()
    app.run(
        debug=bool(os.getenv("DEBUG")),
        port=int(os.getenv("PORT"))
    )
