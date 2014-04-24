from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from game.models import TeamRival, PlayerModel, Team


def players(request, pos, sort_by, page_num):
    if pos=='all':
        players =  PlayerModel.objects.all().order_by(sort_by).reverse()
    elif pos=='CEN':
        players =  PlayerModel.objects.all().filter(POS='Center').order_by(sort_by).reverse()
    elif pos=='PG':
        players =  PlayerModel.objects.all().filter(POS='Point Guard').order_by(sort_by).reverse()
    elif pos=='SG':
        players =  PlayerModel.objects.all().filter(POS='Shooting Guard').order_by(sort_by).reverse()
    elif pos=='PF':
        players =  PlayerModel.objects.all().filter(POS='Power Forward').order_by(sort_by).reverse()
    elif pos=='SF':
        players =  PlayerModel.objects.all().filter(POS='Small Forward').order_by(sort_by).reverse()
    pages_num = len(players) / 10
    last_page_num = len(players) % 10
    if last_page_num>0:
        pages_num += 1
    if int(page_num) == pages_num:
        page_players = players[(int(page_num)-1)*10:len(players)]
    else:
        page_players = players[(int(page_num)-1)*10:int(page_num)*10]
    context = {'pages_range':range(pages_num), 'pos':pos, 'players':page_players, 'sort_by':sort_by, 'page_num':page_num}
    return render(request, 'game/players.html', context)


def teams(request):
    context = {'teams_atlantic': Team.objects.all().filter(Q(name='BOS') | Q(name='BKN') | Q(name='NYK')| Q(name='PHI')| Q(name='TOR')),
               'teams_central':Team.objects.all().filter(Q(name='CHI') | Q(name='CLE') | Q(name='DET')| Q(name='IND')| Q(name='MIL')),
               'teams_southeast':Team.objects.all().filter(Q(name='ATL') | Q(name='CHA') | Q(name='MIA')| Q(name='ORL')| Q(name='WAS')),
               'teams_southwest':Team.objects.all().filter(Q(name='DAL') | Q(name='HOU') | Q(name='MEM')| Q(name='NOH')| Q(name='SAS')),
               'teams_northwest':Team.objects.all().filter(Q(name='DEN') | Q(name='MIN') | Q(name='OKC')| Q(name='POR')| Q(name='UTA')),
               'teams_pacific':Team.objects.all().filter(Q(name='GSW') | Q(name='LAC') | Q(name='LAL')| Q(name='PHX')| Q(name='SAC'))}
    return render(request, 'game/teams.html', context)


def play(request):
    if request.method == 'POST':
        sg1 = request.POST.get('sg1', '')
        pg1 = request.POST.get('pg1', '')
        sf1 = request.POST.get('sf1', '')
        pf1 = request.POST.get('pf1', '')
        c1 = request.POST.get('c1', '')
        sg2 = request.POST.get('sg2', '')
        pg2 = request.POST.get('pg2', '')
        sf2 = request.POST.get('sf2', '')
        pf2 = request.POST.get('pf2', '')
        c2 = request.POST.get('c2', '')

        players = [get_player_data(sg1),get_player_data(pg1),get_player_data(sf1),get_player_data(pf1),get_player_data(c1),
                   get_player_data(sg2),get_player_data(pg2),get_player_data(sf2),get_player_data(pf2),get_player_data(c2)]

        team1_scores = {players[0]:sg_score(players[0]),players[1]:pg_score(players[1]),players[2]:sf_score(players[2]),players[3]:pf_score(players[3]),players[4]:center_score(players[4])}
        team2_scores = {players[5]:sg_score(players[5]),players[6]:pg_score(players[6]),players[7]:sf_score(players[7]),players[8]:pf_score(players[8]),players[9]:center_score(players[9])}

        team1 = team1_scores.values()
        team2 = team2_scores.values()
        team1_score = sum(team1)
        team2_score = sum(team2)

        return render(request, 'game/result.html', {'team1': team1_scores, 'team1_score':team1_score, 'team2': team2_scores,'team2_score':team2_score})
    return render(request, 'game/play.html')


def search(request):
    if request.method == 'POST':
        player_name = request.POST.get('pname', '')
        player = get_player_data(player_name)
        if player.POS == "Center":
            score = center_score(player)
        elif player.POS == "Power Forward":
            score = pf_score(player)
        elif player.POS == "Small Forward":
            score = sf_score(player)
        elif player.POS == "Point Guard":
            score = pg_score(player)
        else:
            score = sg_score(player)
        return render(request, 'game/player_detail.html', {'player': player, 'score':score})
    return render(request, 'game/search.html')

def player_detail(request, player_id):
    player = get_object_or_404(PlayerModel, pk=player_id)

    if player.POS == "Center":
        score = center_score(player)
    elif player.POS == "Power Forward":
        score = pf_score(player)
    elif player.POS == "Small Forward":
        score = sf_score(player)
    elif player.POS == "Point Guard":
        score = pg_score(player)
    else:
        score = sg_score(player)

    return render(request, 'game/player_detail.html', {'player': player, 'score':score})

def team_detail(request, team_id, page_num):
    team = get_object_or_404(Team, pk=team_id)
    games = get_team_games(team.name)

    pages_num = len(games) / 10
    last_page_num = len(games) % 10
    if last_page_num>0:
        pages_num += 1
    if int(page_num) == pages_num:
        page_games = games[(int(page_num)-1)*10:len(games)]
    else:
        page_games = games[(int(page_num)-1)*10:int(page_num)*10]
    context = {'pages_range':range(pages_num), 'team': team, 'team_id':team_id, 'games':page_games, 'page_num':page_num}

    return render(request, 'game/team_detail.html', context)

#utility methods
def get_player_data(player_name):
    p = PlayerModel.objects.all().filter(PLAYER_NAME=player_name)[:1].__getitem__(0)
    return p

def get_team_games(team_name):
    games = TeamRival.objects.all().filter(TEAM_NAME=team_name)
    return games

def get_oreb_pct(p):
    return p.OREB/p.GP

def get_dreb_pct(p):
    return p.DREB/p.GP

def get_stl_pct(p):
    return p.STL/p.GP

def get_pf_pct(p):
    return p.PF/p.GP

def get_ast_pct(p):
    return p.AST/p.GP

def sg_score(p):
    k = [8.36580434731,7.96253363313,-1.67468640962,0.0835260442149,-0.627489778526,1.69095874933,
         -0.205121979924,0.198064272251,0.804302465622,0.194905940799,-0.828816848125]

    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def sf_score(p):
    k = [16.7472252444,4.76201937315,-1.89195639906,0.0418575316824,-0.309539150103,1.24657357575
         -0.127305729013,0.407977140739,0.0928061597198,0.230666444007,-2.25957965396]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def center_score(p):
    k = [16.2353107297,2.57362021576,0.0157509351431,-0.0513302617805,0.256730461643,0.187323060141,
         0.0678709721971,0.848575887295,-1.07555653494,0.482474965147,-3.72922945464]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def pf_score(p):
    k = [11.8696614053,3.34166094703,-0.832639152143,0.0643418423023,-0.601782852871,
         0.224886699464,0.134142422526,0.247000248527,0.400505168254,0.442851459543,-3.98379866329]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def pg_score(p):
    k = [15.1307330176,6.59470508645,-2.00877340401,0.0302439538857,-0.29644026405,0.103340920357,
         -0.494175542653,0.173483735633,0.580577590303,0.096530387138,2.09663002458]

    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))



# class PlayersView(generic.ListView):
#     template_name = 'game/players.html'
#     context_object_name = 'players'
#
#     def get_queryset(self):
#         return PlayerModel.objects.all()
#
# class TeamsView(generic.ListView):
#     template_name = 'game/teams.html'
#     context_object_name = 'teams'
#
#     def get_queryset(self):
#         return Team.objects.all()
#
# class PlayerDetailView(generic.DetailView):
#     model = PlayerModel
#     template_name = 'game/player_detail.html'
#
# class TeamRivalDetailView(generic.DetailView):
#     model = TeamRival
#     template_name = 'game/team_detail.html'
