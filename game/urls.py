from django.conf.urls import patterns, url
from game import views
"""
urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index.html, name='index.html'),
    # ex: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
"""
urlpatterns = patterns('',
    url(r'^$', views.play, name='play'),
    url(r'^result/$', views.play, name='result'),
    url(r'^search/$', views.search, name='search'),
    url(r'^players/(?P<pos>\w+)/(?P<sort_by>\w+)/(?P<page_num>\d+)/$', views.players, name='players'),
    url(r'^teams/$', views.teams, name='teams'),
    url(r'^player/(?P<player_id>\d+)/$', views.player_detail, name='player_detail'),
    url(r'^team/(?P<team_id>\d+)/(?P<page_num>\d+)/$', views.team_detail, name='team_detail'),
)