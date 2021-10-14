from rest_framework import serializers
from .models import Pokemon, Stat, Evolution


class StatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = [
            'name',
            'base_stat',
        ]


class PokemonPrevolutionSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField()
    name = serializers.CharField(max_length=25)
    evolution_type = serializers.CharField(
        max_length=20, 
        default="prevolution"
    )


class PokemonEvolutionSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField()
    name = serializers.CharField(max_length=25)
    evolution_type = serializers.CharField(
        max_length=20,
        default="evolution"
    )


class PokemonSerializer(serializers.ModelSerializer):
    stats = StatSerializer(many=True, read_only=True)
    evolutions = serializers.SerializerMethodField()

    class Meta:
        model = Pokemon
        fields = [
            'pokemon_id',
            'name',
            'height',
            'weight',
            'stats',
            'evolutions',
        ]
    
    def get_evolutions(self, pokemon):
        evolutions = []
        try:
            prevolution = Evolution.objects.get(evolves_to__name=pokemon)
            prevolution_serializer = PokemonPrevolutionSerializer(prevolution.pokemon)
            evolutions.append(prevolution_serializer.data)
        except Exception as e:
            pass

        try:
            evolution = Evolution.objects.get(pokemon__name=pokemon)
            evolution_serializer = PokemonEvolutionSerializer(evolution.evolves_to)
            evolutions.append(evolution_serializer.data)
        except Exception as e:
            pass

        return evolutions
