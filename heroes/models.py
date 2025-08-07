from django.db import models

class HeroModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    intellegence = models.IntegerField()
    strength = models.IntegerField()
    speed = models.IntegerField()
    power = models.IntegerField()

    def __str__(self):
        return self.name
