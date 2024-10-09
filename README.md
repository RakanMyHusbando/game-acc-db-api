
# !!! Warning !!!
This project is still very much a work in progress. Furthermore, it does not yet have any error handling and does not check any regx.
---
# Description
Go to the project folder in the terminal and run:
``` bash
python main.py
```
# API requests
Replace `<game>` with league_of_legends or valorant.
## POST new user
```
http://172.0.0.1:5000/api/user
```
### req-body:
```
{
  "user_name": string,
  "discord_id": string|null
}
```
## POST new game account
```
http://172.0.0.1:5000/api/user?game=<game>
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
### `valorant` req-body:
```
{
  "user_name": string,
  "discord_id": null|string,
  "ingame_name": string,
  "region": string,
}
```
## GET game accounts
```
http://172.0.0.1:5000/api/<game>
```
## GET game account by username
- replace `<user_name>`
```
http://172.0.0.1:5000/api/<game>?username=<user_name>
```
