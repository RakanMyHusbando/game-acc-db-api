from flask import Flask, request, jsonify
from models import Schema
from services import UserService

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
    return jsonify(UserService().get(request.args.get("username")))


@app.route("/api/<string:game>",methods = ["GET"])
def get_game_user(game:str):
    username = request.args.get("username")
    if game == "league_of_legends":
        return jsonify(UserService().get_league_of_legends(username)), 200
    elif game == "valorant":
        return jsonify(UserService().get_valorant(username)), 200

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
