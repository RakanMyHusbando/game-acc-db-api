# user

## POST new user
```
http://172.0.0.1:5000/user
```
Header-data format:
```
{
  user_name: string,
  discord_id: string|null
}
```
## POST new game account
Replace `<game>` with:
  - league_of_legends
  - valorant
```
http://172.0.0.1:5000/user?game=<game>
```
