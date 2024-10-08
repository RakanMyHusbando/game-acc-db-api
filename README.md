### POST: 'user_league_of_legends' (add new league acc)
```bash
http://host:port/user/league_of_legends
```
### GET: all accounts for a game (by username) 
Games:
    league_of_legends
    valorant
```bash
http://host:port/user/<game>/<username>
```
### GET: all 'user_league_of_legends' (all league accs but no user.name)
```bash
http://host:port/user/league_of_legends/*
```

