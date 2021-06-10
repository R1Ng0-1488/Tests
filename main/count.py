class Count:

	def __init__(self, request, testset_id):
		self.testset_id = str(testset_id)
		self.session = request.session
		count = self.session.get(self.testset_id)
		if not count:
			self.session[self.testset_id] = {'true': 0, 'false': 0, 'state': True}
			count = self.session[self.testset_id]
		self.count = count

	def clear_info(self, info):
		'''get request.POST return answer'''
		arr_answer = []

		for i in info:
			arr_answer.append(i['test'].answer_set.filter(answer=i['answer']).first().is_true == i['answer_is_true'])
		
		answer = all(arr_answer)
		return answer

	def write_down(self, answer):
		'''if the answer is true add to session +1'''
		if answer:
			self.session[self.testset_id]['true'] += 1
		else:
			self.session[self.testset_id]['false'] += 1
		self.session.modified = True

	def clear(self):
		'''tidy up the session'''
		self.session[self.testset_id]['true'] = 0
		self.session[self.testset_id]['false'] = 0
		self.session[self.testset_id]['state'] = True
		self.session['finish'] = ''
		self.session.modified = True

	def get_next(self, info, maximum):
		'''get the next question'''
		current_order = info[0]['test'].order
		if current_order == maximum - 1:
			return False
		return current_order + 1

	def get_persent(self, what):
		'''get percents'''
		total = self.session[self.testset_id]['true'] + self.session[self.testset_id]['false']
		if total != 0:
			if what == 'true':
				return round(self.session[self.testset_id]['true'] / total * 100, 2)
			else:
				return round(self.session[self.testset_id]['false'] / total * 100, 2)

	def finish(self):
		'''mark if it finished'''
		self.session['finish'] = self.testset_id