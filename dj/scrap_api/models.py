from django.db import models

# Create your models here.
#

from django.db import models


class CricketMatch(models.Model):
    teams = models.CharField(max_length=100)
    tournament = models.CharField(max_length=100)
    score = models.CharField(max_length=100)
    sport = models.CharField(max_length=50, default="cricket")

    def __str__(self):
        return self.teams
