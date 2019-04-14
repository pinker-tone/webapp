from django.urls import path
from django.urls import include
from .views import *

urlpatterns = [
    path('games/', GameView.as_view()),
    path('games/history/', GameHistoryView.as_view()),
    path('games/giveanswers/', GameWaitingView.as_view()),
    path('games/end/', GameEndView.as_view()),
    path('users/', UsersView.as_view()),
]
