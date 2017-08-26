from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import random as r
import csv

author = 'Jonas Mueller Gastell & Yucheng Liang'

doc = """
Experiment to Test Updating on Ability
"""


class Constants(BaseConstants):
	name_in_url = 'experiment'
	players_per_group = None
	num_rounds = 1
	test = "raven"
	test_minutes = 5

	correct_point = 3
	wrong_point = -1

	with open('updatingOnAbility_tests/raven.csv') as f:
		questions = list(csv.DictReader(f))

	num_rounds = len(questions)

class Subsession(BaseSubsession):
	def before_session_starts(self):
		if self.round_number == 1:
			for p in self.get_players():
				# p.participant.vars['questions'] = Constants.questions
				p.participant.vars['questions'] = r.sample(Constants.questions, len(Constants.questions))
				p.score = 0

		for p in self.get_players():
			question_data = p.current_question()
			p.question_id = question_data['id']
			p.solution = question_data['solution']
			p.num_choices = question_data['num_choices']



class Group(BaseGroup):
	pass


class Player(BasePlayer):
	question_id = models.PositiveIntegerField()
	num_choices = models.PositiveIntegerField()
	solution = models.CharField()
	score = models.FloatField()
	submitted_answer = models.PositiveIntegerField(widget=widgets.RadioSelect())
	is_correct = models.BooleanField()
	## These are variables of players, so they need to be defined under Player. Their values will either be assigned in Subsession or submitted through forms.

	def current_question(self):
		return self.participant.vars['questions'][self.round_number - 1]
	## current_question need not be stored in the result table

	def check_correct(self):
		self.is_correct = self.submitted_answer == self.solution
		if self.is_correct:
			self.score += Constants.correct_point
		else:
			self.score += Constants.wrong_point
