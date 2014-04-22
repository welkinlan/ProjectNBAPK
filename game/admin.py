from django.contrib import admin
from game.models import PlayerModel, TeamRival, Team

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('PLAYER_NAME', 'GP', 'PTS')
    """
    list_filter = ['pub_date']
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    search_fields = ['question']
    """

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    """
    list_filter = ['pub_date']
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    search_fields = ['question']
    """

class TeamRivalAdmin(admin.ModelAdmin):
    list_display = ('TEAM_NAME', 'RIVAL_NAME', 'PLACE')
    """
    list_filter = ['pub_date']
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    #inlines = [ChoiceInline]
    search_fields = ['question']
    """

admin.site.register(PlayerModel, PlayerAdmin)
admin.site.register(TeamRival, TeamRivalAdmin)
admin.site.register(Team, TeamAdmin)