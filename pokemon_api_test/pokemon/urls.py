from django.urls import path
from . views import PokemonView, PokemonsView


urlpatterns = [
    path('pokemons/', PokemonsView.as_view()),
    path('pokemon/<str:name>', PokemonView.as_view()),
]