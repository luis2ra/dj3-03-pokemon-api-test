from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import Pokemon
from . serializers import PokemonSerializer

# Create your views here.
class PokemonsView(APIView):

    def get_queryset(self):
        return Pokemon.objects.all()

    def get(self, request):
        serializer = PokemonSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PokemonView(APIView):

    def get_queryset(self, name):
        return get_object_or_404(Pokemon, name=name)

    def get(self, request, name):
        serializer = PokemonSerializer(self.get_queryset(name))
        return Response(serializer.data, status=status.HTTP_200_OK)
