from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class prior(Page):
	form_model = models.Player
	form_fields = ['prior']
	def is_displayed(self):
		return self.round_number == 1
	def before_next_page(self):
		self.player.participant.vars['previous_belief'] = self.player.prior   # CUSTOMIZE THIS


class info1(Page):
	form_model = models.Player
	form_fields = ['CertainVSNoInfo','CertainVSImperfect','ImperfectVSNoInfo','Asym1VSAsym2']
	# def vars_for_template(self):
	# 	return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["NoInfo"], "right_side_amounts": Constants.right_side_amounts}


class posterior(Page):
	form_model = models.Player
	form_fields = ['posterior']
	def vars_for_template(self):
		return {'info_select': Constants.NameDict[self.player.info_select], 'signal_good': self.player.signal_good, 'previous_belief': self.player.participant.vars['previous_belief']}
	def before_next_page(self):
		self.player.participant.vars['previous_belief'] = self.player.posterior  # CUSTOMIZE THIS


page_sequence = [
	prior,
	info1,
	posterior,
]

