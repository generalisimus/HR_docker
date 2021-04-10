from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from .utilities import get_timestamp_path

class AdvUser(AbstractUser):
	is_manager = models.BooleanField(default=False)


class Poll(models.Model):
	VIEWS = (
		(None, 'Выберите тип опроса'),
		('Test', 'Тест'),
		('Poll', 'Опрос'),
	)

	view = models.CharField(max_length=4, choices=VIEWS)
	title = models.CharField(max_length=50)
	description = models.TextField(verbose_name='описание опроса')
	date_relise = models.DateTimeField()
	is_active = models.BooleanField()
	is_timer = models.BooleanField(verbose_name='таймер')
	

	def __str__(self):
		return self.title

	class Meta:
		verbose_name='Опрос'
		verbose_name_plural='Опросы'

class Question(models.Model):
	VIEWS = (
		(None, 'Выберите тип ответа на вопрос'),
		('r', 'Выбор одного ответа'),
		('c', 'Выбор нескольких ответов'),
	)
	poll = models.ManyToManyField(Poll, related_name='poll_table')
	polls_one = models.ForeignKey(Poll, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	view = models.CharField(max_length=1, choices=VIEWS)
	# image = models.ImageField(verbose_name='Изображение', blank=True)
	timer = models.IntegerField(verbose_name='кол-во секунда на ответ', default=0)

	def __str__(self):
		return self.title


	class Meta:
		verbose_name='Вопрос'
		verbose_name_plural = 'Вопросы'

class QuestionImage(models.Model):
	question_image = models.ForeignKey(Question, on_delete=models.CASCADE)
	images = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	title = models.TextField()
	score = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name='Ответ'
		verbose_name_plural='Ответы'

class QuestionList(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	weight = models.IntegerField()

	def __self__(self):
		return self.weight


class AnswerUser(models.Model):
	user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
	question = models.ForeignKey(QuestionList, on_delete=models.CASCADE)
	answer = models.ManyToManyField(Answer)


class ResultsAll(models.Model):
	name_user = models.CharField(max_length=100)
	id_user = models.IntegerField()
	poll_total = models.CharField(max_length=200)	
	total = models.IntegerField(default=0)

	def __str__(self):
		return self.poll_total

	class Meta:
		ordering = ['-id']
		verbose_name='Результат'
		verbose_name_plural='Результаты'


class Result(models.Model):
	name_user = models.CharField(max_length=100)
	id_user = models.IntegerField()
	answer_total = models.TextField()
	question_total = models.CharField(max_length=100)
	poll_total = models.CharField(max_length=100)
	total = models.IntegerField(default=0)

	def __str__(self):
		return self.question_total

	class Meta:

		verbose_name = 'Детальный ответ'
		verbose_name_plural = 'Детальные ответы'


