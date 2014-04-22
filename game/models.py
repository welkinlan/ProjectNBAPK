from django.db import models

# Create your models here.
class PlayerModel(models.Model):

    PLAYER_NAME = models.CharField(max_length=100) #name
    GP = models.FloatField() #game played
    MIN = models.FloatField() #minutes played
    PTS = models.FloatField() # points made
    
    FGM = models.FloatField()
    FGA = models.FloatField()
    FG_PCT = models.FloatField() #field goals percent
    
    FG3M= models.FloatField()
    FG3A = models.FloatField()
    FG3_PCT = models.FloatField() #3 point goals percent
    
    FTM = models.FloatField()
    FTA = models.FloatField()
    FT_PCT = models.FloatField() #free throw percentage
    
    OREB = models.FloatField()
    DREB = models.FloatField()
    REB = models.FloatField() #rebounds
    
    AST = models.FloatField() #assist
    STL = models.FloatField() #steal
    BLK = models.FloatField() #block
    TOV = models.FloatField() #turnover
    PF = models.FloatField() #personal fouls

    AST_TOV = models.FloatField()
    STL_TOV = models.FloatField()
    
    EFG_PCT = models.FloatField() #effective field goal percent
    TS_PCT = models.FloatField() #true shooting percent

    POS = models.CharField(max_length=100)
    
    def __str__(self):
        return self.PLAYER_NAME

class TeamRival(models.Model):

    TEAM_NAME = models.CharField(max_length=3) #team name
    RIVAL_NAME = models.CharField(max_length=3) #rival name
    PLACE = models.CharField(max_length=3) #vs or @
    WL = models.CharField(max_length=1) #win(w) or lose(l)
    MIN = models.FloatField() #game minutes
    
    FGM = models.FloatField()
    FGA = models.FloatField()
    FG_PCT = models.FloatField() #field goals percent

    FG3M= models.FloatField()
    FG3A = models.FloatField()
    FG3_PCT = models.FloatField() #3 point goals percent

    FTM = models.FloatField()
    FTA = models.FloatField()
    FT_PCT = models.FloatField() #free throw percentage

    OREB = models.FloatField()
    DREB = models.FloatField()
    REB = models.FloatField() #rebounds
    
    AST = models.FloatField() #assist
    STL = models.FloatField() #steal
    BLK = models.FloatField() #block
    TOV = models.FloatField() #turnover
    PF = models.FloatField() #personal fouls

    PTS = models.FloatField() #points made
    
    def __str__(self):
        return self.TEAM_NAME + self.PLACE + self.RIVAL_NAME


class Team(models.Model):
    name = models.CharField(max_length=3)
    #desc = models.CharField(max_length=100)

    def __str__(self):
        return self.name