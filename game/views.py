from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms

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
    k = [10.1403591813,7.92559928021,-1.68368876644,0.0834489958525,-0.622774178923,
         1.70145212393,-0.210151603144,0.192846506111,0.817867801501,0.185498627276,-2.35985106413]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def sf_score(p):
    k = [2.31357214435,1.23401901957,-0.302822154469,0.0848033354795,-0.479812576028
         ,1.15199335691,-0.0563046747834,0.257127051968,0.609417861421,0.198950507681,0.804194964276]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def center_score(p):
    k = [11.6941404569,3.63422088394,-1.03033055845,0.073550659118,-0.684033825639,0.187323060141,
         0.210258659901,0.135103154902,0.641899331065,0.373386483615,-4.55259513626]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def pf_score(p):
    k = [3.30807330038,3.97567645514,-1.11105494761,0.080384144615,-0.748293961234,
         0.198142217051,0.211008507083,0.113389461421,0.671075643291,0.377207935153,1.41185652658]
    item = [p.EFG_PCT,p.TS_PCT,p.FT_PCT,p.FG3_PCT,p.AST_TOV,p.STL_TOV,
            get_oreb_pct(p),get_dreb_pct(p),get_ast_pct(p),get_stl_pct(p),get_pf_pct(p)]
    return sum (x*y for x,y in zip(k,item))

def pg_score(p):
    k = [17.378548515,6.40513899395,-2.03875291709,0.0286505313115,-0.287807917523,2.22424746262,
         -0.495853544328,0.171749597936,0.59026216528,0.096530387138,0.542013007401]
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
