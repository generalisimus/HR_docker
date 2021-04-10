from django.contrib import admin

from .models import *
from .forms import *


# class QuestionInline(admin.TabularInline):
# 	model = Question
# 	fields = '__all__'
class QuestionImageInline(admin.TabularInline):
	model = QuestionImage
	fields = ('images',)
	extra = 1

class AnswerInline(admin.TabularInline):
	model = Answer
	fields = ('question', 'title', 'score')
	extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline, QuestionImageInline]
	list_display = ('title', 'view',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
	list_display = ('name_user', 'id_user', 'question_total', 'poll_total', 'answer_total', 'total')
	search_fields = ('name_user','poll_total')
	list_filter = ('poll_total',)

@admin.register(ResultsAll)
class ResultAllAdmin(admin.ModelAdmin):
	list_display = ('name_user', 'poll_total', 'total')


admin.site.register(AdvUser)
admin.site.register(QuestionList)
admin.site.register(Poll)




