from flask import Flask, request
from models import Schema
from services import UserService
from utils import UtilsMain

utils = UtilsMain()
app = Flask(__name__)

@app.route("/api/user",methods = ["POST"])
def create():
    game = request.args.get("game")
    if not game:
        return UserService().create(request.get_json()), 201
    elif game == "league_of_legends":
        return UserService().create_league_of_legends(request.get_json()), 201
    elif game == "valorant":
        return UserService().create_valorant(request.get_json()), 201

@app.route("/api/user",methods = ["GET"])
def get():
    username = request.args.get("username")
    result = UserService().get(username)
    return utils.res_get(result)

@app.route("/api/<string:game>",methods = ["GET"])
def get_game_user(game:str):
    username = request.args.get("username")
    result = None
    if game == "league_of_legends":
        result = UserService().get_league_of_legends(username)
    elif game == "valorant":
        result =  UserService().get_valorant(username)
    return utils.res_get(result)


if __name__ == "__main__":
    Schema()
    app.run(debug=True)
