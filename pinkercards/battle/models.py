from django.db import models

from django.contrib.auth.models import User

class Questions(models.Model):
    '''Модель таблицы вопросов'''

    question_text = models.CharField(max_length=1000)
    answer = models.CharField(max_length=20)
    question_type = models.CharField(max_length=20, unique=False)

    def __str__(self):
        return 'text: {}, answer: {}, type: {}.'.format(self.question_text, self.answer, self.question_type)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

class Game(models.Model):
    '''Модель таблицы игр'''

    user_1 = models.ForeignKey(User, verbose_name="User 1", related_name="user_1", on_delete=models.DO_NOTHING, unique=False)
    user_2 = models.ForeignKey(User, verbose_name="User 2", related_name="user_2", on_delete=models.DO_NOTHING, unique=False)
    questions = models.ManyToManyField(Questions, verbose_name="Questions", related_name="question")
    status = models.CharField(max_length=20, unique=False, default='WAITING')
    # hash = models.CharField(max_length)
    date = models.DateTimeField("Create date", auto_now_add=True)

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

class GameHistory(models.Model):
    '''Модель таблицы истории игр'''

    game = models.ForeignKey(Game,  verbose_name="Game", related_name="game", on_delete=models.CASCADE)
    winner = models.ForeignKey(User,  verbose_name="Winner", related_name="winner", on_delete=models.PROTECT, blank=True, null=True)
    answers_correct_user_1 = models.SmallIntegerField(unique=False)
    answers_correct_user_2 = models.SmallIntegerField(unique=False, blank=True, null=True)
    class Meta:
        verbose_name = "Game History"
        verbose_name_plural = "Games History"
