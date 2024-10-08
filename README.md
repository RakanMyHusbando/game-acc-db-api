---
Replace `<game>` with:
  - league_of_legends
  - valorant
---
## POST new user
```
http://172.0.0.1:5000/api/user
```
### Header data:
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
### `league_of_legemds` header data:
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
- if no user with this `user_name` exists, it will be created
- `position` max length is 2
- `position[i].champs` max length is 3
### `valorant` header data:
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
