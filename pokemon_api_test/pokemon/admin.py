from django.contrib import admin
from .models import (
    Pokemon,
    Stat,
    Evolution
)

# Register your models here.
@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    model = Pokemon


@admin.register(Stat)
class PokemonAdmin(admin.ModelAdmin):
    model = Stat


@admin.register(Evolution)
class PokemonAdmin(admin.ModelAdmin):
    model = Evolution
