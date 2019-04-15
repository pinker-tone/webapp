from rest_framework import serializers
from .models import Game, Questions
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация таблицы юзеров"""

    class Meta:
        model = User
        fields = ("id", "username")


class QuestionsSerializer(serializers.ModelSerializer):
    """Сериализация таблицы вопросов"""

    class Meta:
        model = Questions
        fields = ("id", "question_text", "question_type", "answer")


class GameSerializer(serializers.ModelSerializer):
    """Сериализация таблицы игр"""
    user_1 = UserSerializer()
    user_2 = UserSerializer()
    questions = QuestionsSerializer(many=True)

    class Meta:
        model = Game
        fields = ("id", "user_1", "user_2", "questions", "status", "winner", "answers_correct_user_1", "answers_correct_user_2", "draw", "date")

class GameCreateSerializer(serializers.ModelSerializer):
    """Сериализация таблицы игр"""
    user_1 = UserSerializer()
    user_2 = UserSerializer()
    questions = QuestionsSerializer(many=True)

    class Meta:
        model = Game
        fields = ("user_1", "user_2")
