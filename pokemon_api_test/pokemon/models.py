from django.db import models

# Create your models here.
class Pokemon(models.Model):
    pokemon_id = models.PositiveIntegerField()
    name = models.CharField(
        max_length=25, 
        unique=True
    )
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Stat(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, 
        on_delete=models.CASCADE,
        related_name="stats"
    )
    name = models.CharField(
        max_length=25
    )
    base_stat = models.PositiveIntegerField()

    def __str__(self):
        return str(self.pokemon) + ' - ' + self.name


class Evolution(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="evolution"
    )
    evolves_to = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="evolves_to"
    )

    def __str__(self):
        return str(self.pokemon) + ' > ' + str(self.evolves_to)
