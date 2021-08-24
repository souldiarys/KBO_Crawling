from django.db import models

class Hitter(models.Model):
    player_id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    name = models.CharField(max_length=32, default='-')
    team = models.ForeignKey('Team', models.CASCADE)
    avg = models.CharField(max_length=5, default='-')
    g = models.IntegerField(default=0)
    pa = models.IntegerField(default=0)
    ab = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    number_2b = models.IntegerField(db_column='2b', default=0)
    number_3b = models.IntegerField(db_column='3b', default=0)
    hr = models.IntegerField(default=0)
    rbi = models.IntegerField(default=0)
    bb = models.IntegerField(default=0)
    hbp = models.IntegerField(default=0)
    so = models.IntegerField(default=0)
    gdp = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'hitter'
        unique_together = (('player_id', 'year'),)


class Pitcher(models.Model):
    player_id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    name = models.CharField(max_length=32, default='-')
    team = models.ForeignKey('Team', models.CASCADE)
    era = models.CharField(max_length=5, default='-')
    g = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    l = models.IntegerField(default=0)
    sv = models.IntegerField(default=0)
    hld = models.IntegerField(default=0)
    wpct = models.CharField(max_length=5, default='-')
    ip = models.CharField(max_length=10, default='-')
    h = models.IntegerField(default=0)
    hr = models.IntegerField(default=0)
    bb = models.IntegerField(default=0)
    hbp = models.IntegerField(default=0)
    so = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    er = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'pitcher'
        unique_together = (('player_id', 'year'),)


class Team(models.Model):
    name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'team'