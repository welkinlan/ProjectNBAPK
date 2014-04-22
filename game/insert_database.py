from game.models import Player
import cjson

with open('/game/static/game/json/players.json', 'r') as f:
    for line in f:
        data = cjson.decode(line)
        p = Player(name=data['PLAYER_NAME'], gp=data['GP'], min=data['MIN'], tov=data['TOV'], reb=data['REB'],\
                   fg3a=data['FG3A'], efg=data['EFG_PCT'], ast=data['AST'], ast_tov=data['AST_TOV'], fg3m=data['FG3M'],\
                   oreb=data['OREB'], fgm=data['FGM'], pf=data['PF'], pts=data['PTS'], fga=data['FGA'], ts=data['TS_PCT'],\
                   stl=data['STL'], fta=data['FTA'], blk=data['BLK'], dreb=data['DREB'], ftm=data['FTM'], stl_tov=data['STL_TOV'],\
                   ft=data['FT_PCT'], fg=data['FG_PCT'], fg3=data['FG3_PCT'])
        p.save()
