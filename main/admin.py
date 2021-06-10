from django.contrib import admin

from .forms import BaseAnswerFormSet
from .models import TestSet, Test, Answer

# Register your models here.


class AnswerInline(admin.TabularInline):
	model = Answer
	formset = BaseAnswerFormSet
	extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
	list_display = ('question', 'test_set',)
	inlines = (AnswerInline,)


admin.site.register(TestSet)
