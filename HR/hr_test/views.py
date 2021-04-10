from django.shortcuts import render, redirect, get_object_or_404, loader
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.db.models import Sum, Max, Min
from django.db.models import Q


from HR.settings import *
from .models import *
from .forms import *
from datetime import datetime
from datetime import date
from datetime import timedelta
import time

def register(request):
	"""Регистрация нового пользователя"""
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		email = request.POST.get('email').lower()
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if AdvUser.objects.filter(email=request.POST.get('email')).exists()	or \
			AdvUser.objects.filter(email__iexact=request.POST.get('email')):
			messages.error(request, message='Пользователь с таким адресом' + 
											' электронной почты уже существует')
			form = UserRegisterForm()
			return render(request, 'registration/registration_form.html', 
															{'form': form})
		if AdvUser.objects.filter(username=request.POST.get('username')).exists():
			messages.error(request, message='Пользователь с таким именем уже существует')
			form = UserRegisterForm()
			return render(request, 'registration/registration_form.html',
															 {'form': form})
		if password1 != password2:
			messages.error(request, message='Пароли не совпадают')
			form = UserRegisterForm()
			return render(request, 'registration/registration_form.html',
															 {'form': form})
		if len(password1) < 8 or len(password2) < 8:
			messages.error(request, message='слишком короткий пароль минимум 8 символов')
			form = UserRegisterForm()
			return render(request, 'registration/registration_form.html',
															 {'form': form})	
		elif form.is_valid():
			email = form.cleaned_data['email'].lower()
			form.save()
			return HttpResponseRedirect(reverse_lazy('hr_test:index'))
	else:
		form = UserRegisterForm()
		context = {'form': form}
		return render(request, 'registration/registration_form.html', {'form': form})


def index(request):
	"""Стартовая страница"""
	poll = Poll.objects.filter(date_relise__date__lte=datetime.now())
	result = ResultsAll.objects.all()
	count = {}
	for i in poll:
		count[i.title] = 0
		for a in result:
			if a.poll_total == i.title:
				count[i.title] += 1
	context = {
		'count': count,
		'poll': poll,
	}
	return render(request, 'index.html', context)


def poll_all(request):
	result_all = ResultsAll.objects.filter(id_user=request.user.id)
	result_list = [x for x in result_all]
	poll = Poll.objects.filter(date_relise__date__lte=datetime.now()).exclude(title__in=result_list)
	context = {
		'result_list': result_list,
		'poll': poll,
	}
	return render(request, 'poll/poll_view.html', context)



def answer(request, pk, question_id):
	"""Вывод вопроса"""
	template = loader.get_template('poll/answer.html')
	poll = Poll.objects.get(id=pk)
	question = get_object_or_404(Question, id=question_id)
	questions = Question.objects.filter(poll=poll)
	question_image = QuestionImage.objects.filter(question_image=question)
	if poll.is_timer:
		i = []
		for q in questions:
			i.append(q.timer)
		sum_time = sum(i)
		minutes = int()
		second =  int()
		if questions.count() > 1:
			a = sum_time * 0.75
			minutes = round(a) // 60
			second = round(a) % 60

		else:
			minutes	= round(sum_time) // 60
			second = round(sum_time) % 60
		context = {
			'minutes': round(minutes),
			'second': round(second),
			'poll': poll,
			'question': question,
			'question_image': question_image
		}
		
		return HttpResponse(template.render(context, request))

	else: 
		context = {
			'question': question,
			'poll': poll,
			'question_image': question_image,
		}

		return HttpResponse(template.render(context, request))
	return HttpResponse(template.render(context, request))

def points(request, poll_id, question_id):
	"""Логика вывода следующего вопроса и 
		сохранения данных ответа на одиг вопрос"""
	result = Result.objects.filter(id_user=request.user.id)
	question = get_object_or_404(Question, id=question_id)
	answers = Answer.objects.filter(question=question.id)
	poll = Poll.objects.get(id=poll_id)
	questions = Question.objects.filter(polls_one=poll)

	list_result = []
	for i in result:
		list_result.append(i.question_total)
	if question.title in list_result:
		a = messages.error(request,	message='Вы уже отвечали на этот вопрос!' +
		' Tест не пройден обратитесь к администратору')
		return render(request, 'index.html', {'a': a})
	question_list_id = []
	for i in questions:
		question_list_id.append(i.id)
	if request.method =='POST' and question.view == 'r':
		if request.POST.get('answer') and question_id in question_list_id:
			Result.objects.create(total = request.POST['answer'],
								name_user = request.user,
								id_user = request.user.id,
								question_total = question.title,
								poll_total = poll.title,
								answer_total = request.POST.get('answer'), 
			)

			question_id = question_id
			
			while True:
				question_id += 1
				if question_id in question_list_id:
					print('no ok')
					return HttpResponseRedirect(reverse('hr_test:answer',
											 args=(poll.id, question_id,)))
				elif question_id > question_list_id[-1]:
					print('ok')
					return HttpResponseRedirect(reverse('hr_test:save', 
									args=(poll.id,)))
				else:
					break
		else:
			messages.error(request, message='Выберете варианты ответа')
			return HttpResponseRedirect(reverse('hr_test:answer', 
								args=(poll.id, question_id,)))
	elif request.method == 'POST' and question.view == 'c':
		if request.POST.get('answer') and question_id in question_list_id:		
			answer_server = request.POST.getlist('answer')
			question_check = []
			for i in answer_server:
				question_check.append(int(i))
			sum_question = sum(question_check)
			Result.objects.create(total = sum_question,
								name_user = request.user,
								id_user = request.user.id,
								question_total = question.title,
								poll_total = poll.title,
								answer_total = request.POST.getlist('answer')
								)
			question_id = question_id
			while True:
				question_id += 1
				if question_id in question_list_id:
					return HttpResponseRedirect(reverse('hr_test:answer',
											 args=(poll.id, question_id,)))
				elif question_id > question_list_id[-1]:
					return HttpResponseRedirect(reverse('hr_test:save', 
										args=(poll.id,)))
				else:
					break
		else:
			messages.error(request, message='Выберете варианты ответа')
			return HttpResponseRedirect(reverse('hr_test:answer', 
								args=(poll.id, question_id,)))
	else:

		return HttpResponseRedirect(reverse('hr_test:answer', 
								args=(poll.id, question_id,)))
	return HttpResponseRedirect(reverse('hr_test:answer', 
								args=(poll.id, question_id,)))

def save(request, poll_id):
	"""Сохранения результатов и расчет баллов за весь опрос"""
	template = loader.get_template('result/result.html')
	polls = Poll.objects.filter(id=poll_id) 
	poll = Poll.objects.get(id=poll_id)
	question = Question.objects.filter(poll__in=polls)
	question_count = question.count()
	result = Result.objects.only('request.user.id').order_by('-id')[:question_count]
	total_sum = result.aggregate(Sum('total'))['total__sum']
	if request.method == 'GET':
		ResultsAll.objects.create(name_user = request.user,
								id_user=request.user.id,
								poll_total=poll.title,
								total = total_sum
								)
		a = HttpResponseRedirect(reverse('hr_test:result', args=(poll.id,)))
	return a

def result(request, poll_id):
	"""Размещена логика расчета результата и отображение результата
	у пользователя"""
	template = loader.get_template('result/result.html')
	polls = Poll.objects.filter(id=poll_id)
	poll = Poll.objects.get(id=poll_id)
	results = ResultsAll.objects.filter(poll_total=poll.title)
	users = AdvUser.objects.all()
	res_user = ResultsAll.objects.filter(poll_total=poll.title).count()
	questions = Question.objects.filter(poll__in=polls).count()
	user = request.user
	result_user = ResultsAll.objects.filter(poll_total=poll.title).get(id_user=user.id)
	result_procent = []
	for r in results:
		result_procent.append(r.total)
	repeat = 0
	while True:
		if result_user.total in result_procent:
			result_procent.remove(result_user.total)
			repeat += 1
		elif result_user not in result_procent:
			result_procent.append(result_user.total)
			repeat -= 1
			break
	result_procent = sorted(result_procent)
	res = result_procent.index(result_user.total) + 1
	result_procent_user = 100 - (res * 100 // len(result_procent))
	poll_question = Question.objects.filter(poll__in=polls)
	poll_answer = Answer.objects.filter(question__in=poll_question)
	data = {
		'res_user': res_user,
		'user': user,
		'result_user': result_user,
		'repeat': repeat,
		'result_procent': result_procent,
		'result_procent_user': result_procent_user,
		'poll': poll,
		'users': users,
	}

	return HttpResponse(template.render(data, request))

class ResultAdmin(View):
	def get(self, request):
		search_query = request.GET.get('search', '')
		result_admin = AdvUser.objects.filter(is_staff=False, is_manager=False)
		if search_query:
			result_admin = AdvUser.objects.filter(is_staff=False, is_manager=False).only('username').filter(username__icontains=search_query)
		# else:
		# 	result_user = short_code.only('poll_total')[:10]		
		# result_list = []
		# for i in result_user:
		# 	result_list.append(i.poll_total)
		# result = Results.objects.filter(poll_total__in=result_list)
		# result_admin = AdvUser.objects.filter(is_staff=False, is_manager=False)
		result = ResultsAll.objects.all()
		context = {
			'result': result,
			'result_admin': result_admin,
		}
		return render(request, 'result/result_admin.html', context)


class ResultAll(View):	
	def get(self, request):
		search_query = request.GET.get('search', '')
		short_code = ResultsAll.objects.filter(id_user=request.user.id)
		if search_query:
			result_user = short_code.only('poll_total').filter(poll_total__icontains=search_query)
		else:
			result_user = short_code.only('poll_total')[:10]		
		result_list = []
		for i in result_user:
			result_list.append(i.poll_total)
		result = Result.objects.filter(poll_total__in=result_list).filter(id_user=request.user.id)
		context = {
			'result': result,
			'result_user': result_user,
			'result_list': result_list,
		}
		return render(request, 'result/result_user.html', context)


class HrLoginView(LoginView):
	"""Вход зарегестрированного пользователя"""
	template_name = 'registration/login.html'


class HrLogoutView(LogoutView):
	"""Выход пользователя"""
	template_name = 'registration/logout.html'
	success_url = reverse_lazy('hr_test: login')

