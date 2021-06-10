from django.db import models


class TestSet(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Test(models.Model):
	order = models.IntegerField(default=0)
	question = models.CharField(max_length=200)
	test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE)

	def __str__(self):
		return self.question

	class Meta:
		ordering = ('order',) 
		unique_together = ('order', 'test_set')


class Answer(models.Model):
	answer = models.CharField(max_length=200)
	is_true = models.BooleanField(default=False)
	test = models.ForeignKey(Test, on_delete=models.CASCADE)

	def __str__(self):
		return self.answer