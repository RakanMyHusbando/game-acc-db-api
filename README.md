# WARNING: This project is in progress and some parts dont work yet!
# Description
Run `python main.py` inside the porject-folder.
# API requests
- replace `<game>` with league_of_legends (or valorant)
- replace `<user_name>` with a username (game-acc or discord-name)
- replace `<discord_id>`
- replace `team_name`
## POST new user
```
http://127.0.0.1:5000/api/user
```
### req-body
```
{
  "user_name": string,
  "discord_id": string|null
}
```
## POST new game account
```
http://127.0.0.1:5000/api/user?game=<game>
```
### `league_of_legemds` req-body:
- if no user with this `user_name` exists, it will be created
- `position` max length is 2
- `position[i].champs` max length is 3
```
{
  "user_name": string,
  "discord_id": null|string,
  "ingame_name": string,
  "position": null|[
    {
      "position": string,
      "champs": [
        null|string
      ]
    }
  ]
}
```
## GET all user
```
http://127.0.0.1:5000/api/user
```
## GET user by username
```
http://127.0.0.1:5000/api/user?username=<user_name>
```
## GET user by discord_id
```
http://127.0.0.1:5000/api/user?discord_id=<discord_id>
```
## GET game accounts
```
http://127.0.0.1:5000/api/user/<game>
```
## GET game account by username
```
http://127.0.0.1:5000/api/user/<game>?username=<user_name>
```
---
## POST new team
```
http://127.0.0.1:5000/api/team
```
### `league_of_legemds` req-body:
```
{
  "team_name": string,
  "game": string,
  "guild_name": null|string,
  "member": null|{
    "role0": string (user_name),
    "role1": string (user_name),
    ...
    "main": {
      "top": string (user_name),
      "jng": string (user_name),
      ...
    },
    "substitute": [
      {
        "name": string (user_name),
        "role": "top"|"jng"|"mid"|"adc"|"sup"
      }
    ]
  }
} 
```
## GET all teams
```
http://127.0.0.1:5000/api/team
```
## GET team by teamname
```
http://127.0.0.1:5000/api/team?teamname=<team_name>
```
