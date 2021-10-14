import environ
import requests
import json

from django.core.management.base import BaseCommand, CommandError
from ...models import Pokemon, Stat, Evolution

env = environ.Env(
    # set casting, default value
    BASE_API_URL=(str, '')
)

# evolution_chain definition
class Command(BaseCommand):
    help = 'Fetch and Store Pokemon Chain - Test'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pokemons_names = []  # List Pokemons Names
        self.BASE_API_URL = env('BASE_API_URL')  # Base Pokemon API

    def add_arguments(self, parser):
        parser.add_argument('chain_id', type=int, help="Evolution Chain ID")

    def fetch_evolution(self, evolution):
        self.pokemons_names.append(evolution[0]["species"]["name"])
        if len(evolution[0]["evolves_to"]) == 0:
            return 'the end'
        self.fetch_evolution(evolution[0]["evolves_to"])

    def fetch_pokemon_data(self, name):
        try:
            request = requests.get(self.BASE_API_URL + "pokemon/" + name)
            response = json.loads(request.content)
            stats = []
            for stat in response["stats"]:
                stats.append({
                    "stat": stat["stat"]["name"],
                    "base_stat": stat["base_stat"]
                })
            return {
                "id": response["id"],
                "name": response["name"],
                "height": response["height"],
                "weight": response["weight"],
                "stats": stats
            }
        except Exception as e:
            raise CommandError('Error processing pokemon data: "%s".' % e)

    def store_pokemon_data(self, data):
        pokemon = Pokemon.objects.filter(pokemon_id = data["id"])

        if not pokemon:
            pokemon = Pokemon(
                pokemon_id = data["id"],
                name = data["name"],
                height = data["height"],
                weight = data["weight"],
            )
            pokemon.save()

            for stat in data["stats"]:
                pokemon_stat = Stat(
                    pokemon = pokemon,
                    name = stat["stat"],
                    base_stat = stat["base_stat"]
                )
                pokemon_stat.save()
        return pokemon
    
    def store_evolution(self, pokemon, evolves_to):
        evolution = Evolution.objects.filter(pokemon__pokemon_id=pokemon.pokemon_id)

        if not evolution:
            pokemon_evolution = Evolution(
                pokemon = pokemon,
                evolves_to = evolves_to
            )
        pokemon_evolution.save()

    def handle(self, *args, **options):
        try:
            request = requests.get(self.BASE_API_URL + "evolution-chain/" + str(options['chain_id']))
            response = json.loads(request.content)

            self.pokemons_names.append(response["chain"]["species"]["name"])
            self.fetch_evolution(response["chain"]["evolves_to"])
            pokemons_objects = []  # List Pokemons Objects
            for key, pokemon in enumerate(self.pokemons_names):
                pokemon_data = self.fetch_pokemon_data(pokemon)
                pokemons_objects.append(self.store_pokemon_data(pokemon_data))
                if key > 0:
                    self.store_evolution(pokemons_objects[key - 1], pokemons_objects[key])

        except Exception as e:
            raise CommandError('Error detail: "%s".' % e)
        self.stdout.write(self.style.SUCCESS('Successfully received data for evolution chain with Id "%s"' % str(options['chain_id'])))
