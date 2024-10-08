import json
from flask import Flask, request, jsonify
from models import Schema
from services import UserLeagueOfLegendsService

app = Flask(__name__)

@app.route("/api/user",methods = ["GET"])
def create_user_league():
    pass

@app.route("/api/user/<string:game>",methods = ["POST"])
def create_user_game(game):
    if game == "league_of_legends":
        print(request.get_json())
        return UserLeagueOfLegendsService().create(request.get_json())   
    elif game == "valorant":
        pass

@app.route("/api/user/<string:game>/<string:username>",methods = ["GET"])
def get_user_game(game,username):
    if game == "league_of_legends":
        return jsonify(UserLeagueOfLegendsService().get(username))

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
