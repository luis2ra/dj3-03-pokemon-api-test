import environ
import requests
import json

from django.core.management.base import BaseCommand, CommandError
#from polls.models import Question as Poll

env = environ.Env(
    # set casting, default value
    BASE_API_URL=(str, '')
)

# evolution_chain definition
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Base Pokemon API
        self.pokemons = []
        self.BASE_API_URL = env('BASE_API_URL')

    def add_arguments(self, parser):
        parser.add_argument('chain_id', type=int, help="Evolution Chain ID")

    def fetch_evolution(self, evolution):
        self.pokemons.append(evolution[0]["species"]["name"])
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
                "weight": response["height"],
                "stats": stats
            }
        except Exception as e:
            raise CommandError('Error processing pokemon data: "%s".' % e)

    def handle(self, *args, **options):
        try:
            request = requests.get(self.BASE_API_URL + "evolution-chain/" + str(options['chain_id']))
            response = json.loads(request.content)

            self.pokemons.append(response["chain"]["species"]["name"])
            self.fetch_evolution(response["chain"]["evolves_to"])
            for key, pokemon in enumerate(self.pokemons):
                pokemon_data = self.fetch_pokemon_data(pokemon)
                print(pokemon_data)
        except Exception as e:
            raise CommandError('Error detail: "%s".' % e)
        self.stdout.write(self.style.SUCCESS('Successfully received data for evolution chain with Id "%s"' % str(options['chain_id'])))
