from django.contrib import admin
from .models import *


class GameAdmin(admin.ModelAdmin):
    """Комнаты чата"""
    list_display = ("user_1", "user_2", "status")

    # def invited_user(self, obj):
    #     return "\n".join([user.username for user in obj.invited_users.all()])

class QuestionsAdmin(admin.ModelAdmin):
    """Комнаты чата"""
    list_display = ("question_text", "answer", "question_type")

admin.site.register(Game, GameAdmin)
admin.site.register(Questions, QuestionsAdmin)
