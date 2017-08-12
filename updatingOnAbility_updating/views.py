from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np

class slider(Page):
	# form_model = models.Player
	# form_fields = ['trial']
	pass

class practice(Page):
	pass

class prior(Page):
	form_model = models.Player
	form_fields = ['prior']
	def is_displayed(self):
		return self.round_number == 1
	def before_next_page(self):
		self.player.participant.vars['previous_belief'] = self.player.prior   # CUSTOMIZE THIS


class info1(Page):
	form_model = models.Player
	form_fields = ['CertainVSNoInfo']
	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["NoInfo"], "right_side_amounts": Constants.right_side_amounts}

class info2(Page):
	form_model = models.Player
	form_fields = ['CertainVSImperfect']
	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["Imperfect"], "right_side_amounts": Constants.right_side_amounts}

class info3(Page):
	form_model = models.Player
	form_fields = ['ImperfectVSNoInfo']
	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Imperfect"], "right_side": Constants.NameDict["NoInfo"], "right_side_amounts": Constants.right_side_amounts}

class info4(Page):
	form_model = models.Player
	form_fields = ['Asym1VSAsym2']
	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Asym1"], "right_side": Constants.NameDict["Asym2"], "right_side_amounts": Constants.right_side_amounts}
	def before_next_page(self):
		self.player.VariableChoiceChooser(self.player.CertainVSNoInfo, self.player.CertainVSImperfect, self.player.ImperfectVSNoInfo, self.player.Asym1VSAsym2)


class info5(Page):
	form_model = models.Player
	form_fields = ['VarChoice']
	def vars_for_template(self):
		return {"left_side": Constants.NameDict[self.player.VarLeft], "right_side": Constants.NameDict[self.player.VarRight], "right_side_amounts": Constants.right_side_amounts}
	def before_next_page(self):
		self.player.ImplementSignal()

class posterior(Page):
	form_model = models.Player
	form_fields = ['posterior']
	def vars_for_template(self):
		return {'info_select': Constants.NameDict[self.player.info_select], 'signal_good': self.player.signal_good, 'previous_belief': self.player.participant.vars['previous_belief']}
	def before_next_page(self):
		self.player.participant.vars['previous_belief'] = self.player.posterior  # CUSTOMIZE THIS


page_sequence = [
	slider,
	practice,
	prior,
	info1,
	info2,
	info3,
	info4,
	info5,
	posterior,
]
