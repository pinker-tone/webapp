from django.contrib import admin
from .models import *


class GameAdmin(admin.ModelAdmin):
    """Игры"""
    list_display = ("id", "user_1", "user_2", "status", "questions", "date")

    def questions(self, obj):
        return ', '.join([question.question_text for question in obj.all()[:5]])

    # def invited_user(self, obj):
    #     return "\n".join([user.username for user in obj.invited_users.all()])

class QuestionsAdmin(admin.ModelAdmin):
    """Воросы"""
    list_display = ("id", "question_text", "answer", "question_type")

admin.site.register(Game, GameAdmin)
admin.site.register(Questions, QuestionsAdmin)
