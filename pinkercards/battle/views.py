from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Game
from .serializers import GameSerializer

class GameView(APIView):
	"""Комнаты чата"""

	def get(self, request, username):
		games = Game.objects.filter(user_1__username=username) | Game.objects.filter(user_2__username=username)
		serializer = GameSerializer(games, many=True)
		return Response({"data": serializer.data})
