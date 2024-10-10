from flask import Flask, request
from models import Schema
from services import UserServices
from utils import UtilsMain

utils = UtilsMain()
app = Flask(__name__)

@app.route("/api/user",methods = ["POST"])
def create():
    game = request.args.get("game")
    if not game:
        return UserServices().create(request.get_json()), 201
    elif game == "league_of_legends":
        return UserServices().create_league_of_legends(), 201
    elif game == "valorant":
        return UserServices().create_valorant(request.get_json()), 201

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
    result = UserServices().get(key,value)
    return utils.res_get(result)

@app.route("/api/<string:game>",methods = ["GET"])
def get_game_user(game:str):
    username = request.args.get("username")
    result = None
    if game == "league_of_legends":
        result = UserServices().get_league_of_legends(username)
    elif game == "valorant":
        result =  UserServices().get_valorant(username)
    return utils.res_get(result)


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
