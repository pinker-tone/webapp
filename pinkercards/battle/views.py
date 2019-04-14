from django.shortcuts import render
from django.http import HttpResponse
from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Game, Questions, GameHistory
from django.contrib.auth.models import User
from .serializers import *

class GameView(APIView):
	"""Все игры пользователя"""
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
		
		if request.data.get("opponent"):
			opponent = request.data.get("opponent")
		else:
			return Response({"status": "Error. opponent field doesnt't exist."})

		if game.is_valid():
			user_1 = request.user
			user_2 = User.objects.filter(username=opponent)
			if user_2.exists():
				if user_1 == user_2[0]:
					return Response({"status": "You are trying to challenge yourself."})
			else:
				return Response({"status": "Error. Opponent \""+opponent+"\" doesn't exist."})

			# creating game object

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

class GameHistoryView(APIView):
	"""История игр"""

	permission_classes = [permissions.IsAuthenticated, ]

	def get(self, request):
		games = GameHistory.objects.filter(game__user_1__username=request.user.username) | GameHistory.objects.filter(game__user_2__username=request.user.username) 
		serializer = GameHistorySerializer(games, many=True)
		return Response({"data": serializer.data})


class GameWaitingView(APIView):
	"""Ответы первого юзера"""

	permission_classes = [permissions.IsAuthenticated, ]

	def post(self, request):
		
		# checking if answers_correct_user_1 exists and valid
		try:
			if int(request.data.get("correct_answers")) in range(1, 6):
				pass
			else:
				return Response({"status": "Error. correct_answers field is invalid."})
		except TypeError:
			return Response({"status": "Error. correct_answers field doesn't exist."})
		
		# checking if game exitsts
		try:
			game_id = int(request.data.get("game_id"))
		except TypeError:
			return Response({"status": "Error. game_id field doesn't exist."})
		if not game_id-1 in range(len(Game.objects.all())):
			return Response({"status": "Error. There's no game with this id."})

		if Game.objects.filter(id=game_id).exists():
			if GameHistory.objects.filter(game__id=game_id).exists():
				return Response({"status": "Error. You've already given answer."})
		else:
			return Response({"status": "Error. This game doesn't exist."})
		
		# checking if it's your game
		if Game.objects.filter(id=game_id, user_1__username=request.user.username).exists():
			pass
		else:
			return Response({"status": "Error. It's not your game."})

		# creating GameHistory object
		game_history = GameHistory()
		game_history.game = Game.objects.get(id=game_id)
		game_history.answers_correct_user_1 = int(request.data.get("correct_answers"))
		game_history.save()

		return Response({"status": "Game successfully added."})

class GameEndView(APIView):
	"""Окончание игры"""

	permission_classes = [permissions.IsAuthenticated, ]

	def post(self, request):
		try:
			game_id = int(request.data.get("game_id"))
		except TypeError:
			return Response({"status": "Error. game field doesn't exist."})
		if not game_id-1 in range(len(Game.objects.all())):
			return Response({"status": "Error. There's no game with this id."})

		# checking if game with given id exists
		if GameHistory.objects.filter(game__id=game_id).exists():
			game = Game.objects.get(id=game_id)
			if game.status == "WAITING":
				if game.user_2.username == request.user.username:
					pass
				else:
					return Response({"status": "Error. It's not your game."})	
			else:
				return Response({"status": "Error. This game is ended."})
		else:
			return Response({"status": "Error. This game doesn't exist or isn't in history."})
		
		# checking if answers_correct field is valid
		try:
			if int(request.data.get("correct_answers")) in range(1, 6):
				pass
			else:
				return Response({"status": "Error. correct_answers field is invalid or doesn't exist."})
		except TypeError:
			return Response({"status": "Error. correct_answers field doesn't exist."})
		

		game_history = GameHistory.objects.get(game__id=game_id)
		game_history.answers_correct_user_2 = int(request.data.get("correct_answers"))
		if game_history.answers_correct_user_1 > game_history.answers_correct_user_2:
			game_history.winner = game_history.game.user_1
		elif game_history.answers_correct_user_1 < game_history.answers_correct_user_2:
			game_history.winner = game_history.game.user_2
		else:
			pass
		game_history.save()
		game.status = "ENDED"
		game.save()
		return Response({"status": "Game successfully ended."})


class UsersView(APIView):
	"""Пользователи"""
	permission_classes = [permissions.AllowAny, ]
	def get(self, request):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response({"data": serializer.data})