# WARNING: This project is in progress and some parts dont work yet!
# API requests
## POST user
```
http://127.0.0.1:5000/api/user
```
#### req-body
```
{
  "user_name": string,
  "discord_id": null|string
}
```
### query param with key "create"
- league_of_legends
#### `league_of_legends` req-body:
- if no user with this "user_name" exists, it will be created
- "position" max length is 2
- "position[i].champs" max length is 3
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
## GET user
```
http://127.0.0.1:5000/api/user
```
### query params with key "property" (list seperated by ",")
- league_of_legends
### query params with key "username"
- username (list seperated by ",")
- teamname (list seperated by ",")
## POST team
```
http://127.0.0.1:5000/api/team
```
#### req-body
```
{
  "team_name": string,
  "game": string,
  "guild_name": null|string,
  "member": null|{
    "role0": string (user_name),
    ...
    "main": {
      "role": string (user_name),
      ...
    },
    "substitute": [
      {
        "name": string (user_name),
        "role": string
      },
      ...
    ]
  }
} 
```
### query param with key "create"
- user
- discord
#### `user` req-body
- if the user is part of the main-team then write his role `main_<role>` 
- if the user is part of the substitutes then write his role `substitute_<role>`
```
{
  "user_name": string,
  "team_name": string,
  "role": string
}
```
#### `discord` req-body
```
{
  "server": string,
  "role": null|{
    "team": null|string,
    "player": null|string,
    "tryout": null|string,
    "coach": null|string
  },
  "catrgory": null|string,
  "channel": null|{
    "team_roaster": null|string,
    "team_chat": null|string,
    "shogun_chat": null|string,
    "team_voice": null|string
  }
}
```
