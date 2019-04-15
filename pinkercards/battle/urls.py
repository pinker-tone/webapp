from django.urls import path
from django.urls import include
from .views import *

urlpatterns = [
    path('games/', GameView.as_view()),
    path('games/<int:game_id>/', GameView.as_view()),
    path('games/create/', GameCreateView.as_view()),
    path('games/answer/', GameAnswerView.as_view()),
    path('users/', UsersView.as_view()),
]
