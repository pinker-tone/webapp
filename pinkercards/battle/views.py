from django.shortcuts import render
from django.http import HttpResponse
from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Game, Questions
from django.contrib.auth.models import User
from .serializers import *

class GameView(APIView):
	"""Все игры пользователя, """
	permission_classes = [permissions.IsAuthenticated, ]
	# permission_classes = [permissions.AllowAny,]

	def random_questions(self, query):
		question_num_list = []
		questions = []
		for i in range(5):
			while True:
				id_num = randint(0, len(query)-1)
				if id_num in question_num_list:
					continue
				else:
					break
			question_num_list.append(id_num)
			questions.append(query[id_num])
		return questions

	
	def get(self, request):
		games = Game.objects.filter(user_1__username=request.user.username) | Game.objects.filter(user_2__username=request.user.username)
		serializer = GameSerializer(games, many=True)
		return Response({"data": serializer.data})
	
	def post(self, request):
		# username = request.data.get("username")
		game = GamePostSerializer(data=request.data, many=True)
		
		if game.is_valid():
			user_1 = request.user
			user_2 = User.objects.filter(username=request.data.get("opponent"))
			if user_2.exists():
				if user_1 == user_2:
					return Response({"status": "You are trying to challenge yourself."})
			else:
				return Response({"status": "opponent \""+request.data.get("opponent")+"\" does not exist."})
			game = Game()
			game.user_1 = user_1
			game.user_2 = user_2[0]
			game.save()
			game.questions.add(*self.random_questions(Questions.objects.all()))

			game.status = "WAITING"
			serializer = GameSerializer(game)
			return Response({"status": "Successfully started.", "data": serializer.data})
		else:
			return Response({"status": "Error. Invalid data."})
