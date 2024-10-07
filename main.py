from flask import Flask, request, jsonify
from models import Schema
from services import UserLeagueService

app = Flask(__name__)

@app.route("/set-user/league",methods = ["POST"])
def create_user_league():
    return UserLeagueService().create(request.get_json())

if __name__ == "__main__":
    Schema()
    app.run(debug=True)
