from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time


class welcome(Page):
	pass

class IRB(Page):
	pass

class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.test_minutes * 60

class Question(Page):
	def get_timeout_seconds(self):
		return self.participant.vars['expiry_timestamp'] - time.time()

	def is_displayed(self):
		return self.participant.vars['expiry_timestamp'] - time.time() > 3

	form_model = models.Player
	form_fields = ['submitted_answer']

	def submitted_answer_choices(self):
		return [k for k in range(1, self.player.num_choices+1)]

	def before_next_page(self):
		if not self.timeout_happened:
			self.player.check_correct()
		
	def vars_for_template(self):
		return {
			'image': 'raven/raven{}.png'.format(self.player.question_id)
		}

page_sequence = [
	# welcome,
	# IRB,
	Start,
	# Question,
]
