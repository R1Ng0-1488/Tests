from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory

from .models import Test, TestSet
from .forms import AnswerFormSet
from .count import Count


class TestSetListView(LoginRequiredMixin, ListView):
	queryset = TestSet.objects.all()

	def render_to_response(self, context, **response_kwargs):
		response = super().render_to_response(context, **response_kwargs)
		print(self.request.session.keys())
		if self.request.session.get('finish'):
			count = Count(self.request, self.request.session.get('finish'))
			count.clear()
		return response


class TestDetailView(LoginRequiredMixin, DetailView, FormView):
	model = Test
	form_class = AnswerFormSet

	def get_initial(self, *args, **kwargs):
		self.object = self.get_object()
		return [{'test': self.object.id, 'answer': answer.answer, 'id': answer.id}
			 for answer in self.object.answer_set.all()]

	def form_valid(self, form):
		current_testset = self.object.test_set
		count = Count(self.request, current_testset.id)
		count.write_down(count.clear_info(form.cleaned_data))

		order = count.get_next(form.cleaned_data, current_testset.test_set.count())

		if order:
			next_test = Test.objects.get(order=order, test_set=current_testset)
			return redirect('test', pk=next_test.id)
		else:
			self.request.session[str(current_testset.id)]['state'] = False
			return redirect('testset', current_testset.id)


class TestSetDetailView(DetailView):
	model = TestSet

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		count = Count(self.request, self.object.id)
		context['true'] = self.request.session[str(self.object.id)]['true']
		context['false'] = self.request.session[str(self.object.id)]['false']
		context['true_percent'] = count.get_persent('true')
		context['false_percent'] = count.get_persent('false')
		count.finish()
		return context

	def render_to_response(self, context, **response_kwargs):
		response = super().render_to_response(context, **response_kwargs)
		if self.request.session[str(self.object.id)]['state']:
			first = self.object.test_set.first()
			return redirect('test', first.id)
		return response