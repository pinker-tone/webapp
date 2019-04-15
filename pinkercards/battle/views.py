from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .error_messages import *

from .models import Game, Questions
from django.contrib.auth.models import User
from .serializers import *
from random import randint

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

	
	def get(self, request, game_id=None):
		if game_id:
			if not game_id-1 in range(len(Game.objects.all())):
				return Response({"status": 400, "data": GAME_DOESNT_EXIST}, status=400)
			games = Game.objects.get(id=game_id)
			serializer = GameSerializer(games)
		else:
			games = Game.objects.filter(user_1__username=request.user.username) | Game.objects.filter(user_2__username=request.user.username)
			if len(games) != 1:
				serializer = GameSerializer(games, many=True)
			else:
				serializer = GameSerializer(games[0])
		return Response({"status": 200, "data": serializer.data})


class GameCreateView(APIView):
	"""Создать игру"""
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
	

	def post(self, request):
		# username = request.data.get("username")
		game = GameCreateSerializer(data=request.data, many=True)
		
		if request.data.get("opponent"):
			opponent = request.data.get("opponent")
		else:
			return Response({"status": 400, "data": OPPONENT_FIELD_DOESNT_EXIST}, status=400)

		if game.is_valid():
			user_1 = request.user
			user_2 = User.objects.filter(username=opponent)
			if user_2.exists():
				if user_1 == user_2[0]:
					return Response({"status": 400, "data": TRYING_TO_CHALLENGE_YOURSELF}, status=400)
			else:
				return Response({"status": 400, "data": OPPONENT_DOESNT_EXIST}, status=400)

			# creating game object

			game = Game()
			game.user_1 = user_1
			game.user_2 = user_2[0]
			game.status = "WAITING"
			game.save()
			game.questions.add(*self.random_questions(Questions.objects.all()))

			serializer = GameSerializer(game)

			return Response({"status": 200, "data": serializer.data})
		else:
			return Response({"status": 400, "data": INVALID_DATA}, status=400)


class GameAnswerView(APIView):
	"""Дать ответ"""

	permission_classes = [permissions.IsAuthenticated, ]

	def post(self, request):
		
		# checking if game exitsts
		try:
			game_id = int(request.data.get("game_id"))
		except TypeError:
			return Response({"status": 400, "data": GAMEID_FIELD_DOESNT_EXIST}, status=400)
		if not Game.objects.filter(id=game_id).exists():
			return Response({"status": 400, "data": GAME_DOESNT_EXIST}, status=400)

		game = Game.objects.get(id=game_id)

		# checking if it's your game
		if game.user_1.username == request.user.username:
			its_user_1 = True
			its_user_2 = False
		elif game.user_2.username == request.user.username:
			its_user_1 = False
			its_user_2 = True
		else:
			return Response({"status": 400, "data": NOT_YOUR_GAME}, status=400)

		# checking if answers_correct exists and valid
		try:
			if int(request.data.get("correct_answers")) in range(6):
				pass
			else:
				return Response({"status": 400, "data": CORRECT_ANSWERS_FIELD_IS_INVALID}, status=400)
		except TypeError:
			return Response({"status": 400, "data": CORRECT_ANSWERS_FIELD_DOESNT_EXIST}, status=400)

		# checking if you've already answered
		if game.status != "ENDED":
			if its_user_1 and (game.answers_correct_user_1 or game.answers_correct_user_1 == 0):
				return Response({"status": 400, "data": ANSWER_ALREADY_GIVEN}, status=400)
			elif its_user_2 and (game.answers_correct_user_2 or game.answers_correct_user_2 == 0):
				return Response({"status": 400, "data": ANSWER_ALREADY_GIVEN}, status=400)
		else:
			return Response({"status": 400, "data": GAME_ENDED}, status=400)

		#adding answers
		if its_user_1:
			game.answers_correct_user_1 = int(request.data.get("correct_answers"))
			if game.answers_correct_user_2 or game.answers_correct_user_2 == 0:
				game.status = "ENDED"
				if game.answers_correct_user_1 > game.answers_correct_user_2:
					game.winner = game.user_1
					game.draw = False
				elif game.answers_correct_user_1 < game.answers_correct_user_2:
					game.winner = game.user_2
					game.draw = False
				else:
					game.draw = True
			game.save()
		else:
			game.answers_correct_user_2 = int(request.data.get("correct_answers"))
			if game.answers_correct_user_1 or game.answers_correct_user_1 == 0:
				game.status = "ENDED"
				if game.answers_correct_user_1 > game.answers_correct_user_2:
					game.winner = game.user_1
					game.draw = False
				elif game.answers_correct_user_1 < game.answers_correct_user_2:
					game.winner = game.user_2
					game.draw = False
				else:
					game.draw = True
			game.save()

		return Response({"status": 200, "data": "Your answers were successfully added."})


class UsersView(APIView):
	"""Пользователи"""
	permission_classes = [permissions.IsAuthenticated, ]
	def get(self, request):
		users = User.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response({"data": serializer.data})