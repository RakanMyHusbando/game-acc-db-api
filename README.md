# WARNING: This project is in progress and some parts dont work yet!
# Description
Run `python main.py` inside the porject-folder.
# API requests
- replace `<game>` with league_of_legends or valorant
- replace `<user_name>` with a username (game-acc or discord-name)
- replace `<discord_id>`
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
  "region": string,
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
### `valorant` req-body
```
{
  "user_name": string,
  "discord_id": null|string,
  "ingame_name": string,
  "region": string,
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
http://127.0.0.1:5000/api/<game>
```
## GET game account by username
```
http://127.0.0.1:5000/api/user/<game>?username=<user_name>
```
