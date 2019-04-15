from django.contrib import admin
from .models import *


class GameAdmin(admin.ModelAdmin):
    """Игры"""
    list_display = ("id", "user_1", "user_2", "status", "questions", "winner", "answers_correct_user_1", "answers_correct_user_2", "draw", "date")

    def questions(self, obj):
        return ', '.join([question.question_text for question in obj.all()[:5]])

    # def invited_user(self, obj):
    #     return "\n".join([user.username for user in obj.invited_users.all()])

class QuestionsAdmin(admin.ModelAdmin):
    """Вопросы"""
    list_display = ("id", "question_text", "answer", "question_type")

# class GameHistoryAdmin(admin.ModelAdmin):
#     """История игр"""
#     list_display = ("id", "game", "winner", "answers_correct_user_1", "answers_correct_user_2")

#     def game(self, obj):
#         return str(obj.game.id)

admin.site.register(Game, GameAdmin)
# admin.site.register(GameHistory, GameHistoryAdmin)
admin.site.register(Questions, QuestionsAdmin)