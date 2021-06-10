from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, BaseModelFormSet, BaseInlineFormSet
from django.forms import formset_factory

from .models import Answer


class AnswerForm(forms.ModelForm):
	answer_is_true = forms.BooleanField(label='', required=False)

	class Meta:
		model = Answer
		fields = ('id', 'answer', 'answer_is_true', 'test')
		widgets = {'test': forms.HiddenInput(),
				   'answer': forms.HiddenInput(),
				   'id': forms.HiddenInput()}


class BaseAnswerModelFormSet(BaseFormSet):
	def clean(self):
		'''checking that is_true at least was once and all values can't be true'''
		if any(self.errors):
			# Don't bother validating the formset unless each form is valid
			# on its own
			return
			
		if all(False if form.cleaned_data.get('answer_is_true') else True for form in self.forms):
			raise ValidationError('At least one answer must be chosen')


AnswerFormSet = formset_factory(AnswerForm, extra=0, formset=BaseAnswerModelFormSet)




class BaseAnswerFormSet(BaseInlineFormSet):
	def clean(self):
		'''checking that is_true at least was once and all values can't be true'''
		if any(self.errors):
			# Don't bother validating the formset unless each form is valid
			# on its own
			return

		if all(form.cleaned_data.get('is_true') for form in self.forms ):
			raise ValidationError("All the answers can't be correct")

		if all(False if form.cleaned_data.get('is_true') else True for form in self.forms):
			raise ValidationError("At least one answer must be correct")

