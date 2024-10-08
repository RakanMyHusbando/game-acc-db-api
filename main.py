from flask import Flask, request, jsonify
from models import Schema
from services import UserService

app = Flask(__name__)

@app.route("/api/user",methods = ["POST"])
def create_user():
    game = request.args.get("game")
    if not game:
        return UserService().create(request.get_json()), 201
    elif game == "league_of_legends":
        return UserService().create_league_of_legends(request.get_json()), 201
    elif game == "valorant":
        pass

@app.route("/api/user",methods = ["GET"])
def create_user():
    pass

@app.route("/api/<string:game>",methods = ["GET"])
def get_user_game(game:str):
    username = request.args.get("username")
    if game == "league_of_legends":
        return jsonify(UserService().get_league_of_legends(username))
    elif game == "valorant":
        pass
    else:
        pass

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
