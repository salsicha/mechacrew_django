from django.db import models


# This was the first thing announced, so leave it in place for compatability a while.
#

class Game(models.Model):
    name = models.CharField(default="Nameless Game", max_length=128)

    def __str__(self):
        return str(self.name)

class Crew(models.Model):
    name = models.CharField(default="Nameless Bob", max_length=36)
    game = models.ForeignKey(Game)
    orders = models.CharField(max_length=512, default=None, null=True, blank=True)
    health = models.FloatField(default=0.0)
    

class Vehicle(models.Model):
    crew = models.ForeignKey(Crew)
    name = models.CharField(default="Some thing.", max_length=360)
    health = models.FloatField(default=0.0)
    rotation = models.FloatField(default=0.0)
    pos_x = models.FloatField(default=0.0)
    pos_y = models.FloatField(default=0.0)
    vel_x = models.FloatField(default=0.0)
    vel_y = models.FloatField(default=0.0)    


class Turret(models.Model):
    crew = models.ForeignKey(Crew)
    vehicle = models.ForeignKey(Vehicle)
    name = models.CharField(default="Some thing.", max_length=360)
    health = models.FloatField(default=0.0)
    max_range = models.FloatField(default=20.0)
    rotation = models.FloatField(default=20.0)
    max_rotation = models.FloatField(default=0.0)    
    damage = models.FloatField(default=1.0)
    ammunition = models.IntegerField(default=10)
    

