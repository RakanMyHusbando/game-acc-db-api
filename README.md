# user
## POST new user
```
http://172.0.0.1:5000/user
```
Header-data format:
```
{
  "user_name": string,
  "discord_id": string|null
}
```
## POST new game account
### Replace `<game>` with:
  - league_of_legends
  - valorant
```
http://172.0.0.1:5000/user?game=<game>
```
### Header-data format:
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
