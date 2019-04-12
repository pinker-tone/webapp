from django.urls import path
from django.urls import include
from .views import *

urlpatterns = [
    path('games/<str:username>/', GameView.as_view()),
]
