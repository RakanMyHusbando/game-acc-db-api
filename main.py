import json
from flask import Flask, request, jsonify
from models import Schema
from services import UserLeagueOfLegendsService

app = Flask(__name__)

@app.route("/user",methods = ["GET"])
def create_user_league():
    pass

@app.route("/user/<string:game>",methods = ["POST"])
def create_user_game(game):
    if game == "league_of_legends":
        print(request.get_json())
        return UserLeagueOfLegendsService().create(request.get_json())   
    elif game == "valorant":
        pass

@app.route("/user/league_of_legends/<string:username>",methods = ["GET"])
def get_user_league_of_legends(username):
    return jsonify(UserLeagueOfLegendsService().get(username))

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
