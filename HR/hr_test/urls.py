from django.urls import path, include
from .views import *

app_name = 'hr_test'

urlpatterns = [
	path('', index, name='index'),
	path('poll/', poll_all, name='poll'),
	path('answer/<int:pk>/<int:question_id>', answer, name='answer'),
	path('accounts/register/', register, name='register'),
	path('answer/<int:pk>', answer, name='answer'),
	path('points/<int:poll_id>/<int:question_id>/', points, name="points"),
	path('save/<int:poll_id>', save, name='save'),
	path('result/<int:poll_id>', result, name= 'result'),
	path('accounts/login/', HrLoginView.as_view(), name='login'),
	path('accounts/logout/', HrLogoutView.as_view(), name='logout'),
	path('result_user/', ResultAll.as_view(), name='result_user'),
	path('result_admin/', ResultAdmin.as_view(), name='result_admin'),
]