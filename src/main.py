from flask import Flask, request
from models.schema import Schema
from services import User, Team
import os, dotenv

dotenv.load_dotenv()

app = Flask(__name__)

########
# USER #
########

@app.route("/api/user",methods = ["POST"])
def user_create():
    return User().create(
        request.get_json(),
        request.args.get("create")
    ) 

@app.route("/api/user",methods = ["GET"])
def user_get():
    username = request.args.get("username")
    discord_id = request.args.get("discord_id")
    props = request.args.get("property")
    search = None
    if username:
        search = ["name",username]
    elif discord_id:
        search = ["discord_id",discord_id]
    if props:
        props = props.split(",")
    return User().get(search,props)

########
# TEAM #
########

@app.route("/api/team",methods = ["POST"])
def team_create():
    return Team().create(
        request.get_json(),
        request.args.get("create")
    )
    
@app.route("/api/team",methods = ["GET"])
def team_get():
    teamname = request.args.get("teamname")
    username = request.args.get("username")
    props = request.args.get("propery")
    search = None
    if username: 
        search = ["user_name",username.split(",")]
    elif teamname:
        search = ["team_name",teamname.split(",")]
    if props: 
        props = props.split(",")
    return Team().get(search,props)

        

if __name__ == "__main__":
    Schema()
    app.run(
        debug=bool(os.getenv("DEBUG")),
        port=int(os.getenv("PORT"))
    )
