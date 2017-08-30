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

class info_overview(Page):
	pass

class CertainNoInfo(Page):
	form_model = models.Player
	form_fields = ['CertainVSNoInfo']

	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["NoInfo"],
				"right_side_amounts": Constants.right_side_amounts}


class CertainImperfect(Page):
	form_model = models.Player
	form_fields = ['CertainVSImperfect', 'Imperfect_good', 'Imperfect_bad']

	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["Imperfect"],
				"right_side_amounts": Constants.right_side_amounts}


class ImperfectNoInfo(Page):
	form_model = models.Player
	form_fields = ['ImperfectVSNoInfo']

	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Imperfect"], "right_side": Constants.NameDict["NoInfo"],
				"right_side_amounts": Constants.right_side_amounts}


class Asym1Asym2(Page):
	form_model = models.Player
	form_fields = ['Asym1VSAsym2', 'Asym1_good', 'Asym1_bad', 'Asym2_good', 'Asym2_bad']

	def vars_for_template(self):
		return {"left_side": Constants.NameDict["Asym1"], "right_side": Constants.NameDict["Asym2"],
				"right_side_amounts": Constants.right_side_amounts}

	def before_next_page(self):
		self.player.VariableChoiceChooser(self.player.CertainVSNoInfo, self.player.CertainVSImperfect,
										  self.player.ImperfectVSNoInfo, self.player.Asym1VSAsym2)


class VarChoice(Page):
	form_model = models.Player
	form_fields = ['VarChoice']

	def vars_for_template(self):
		return {
			"left_side": Constants.NameDict[self.player.VarLeft],
			"right_side": Constants.NameDict[self.player.VarRight],
			"right_side_amounts": Constants.right_side_amounts,
			"firm1": self.player.VarRight == 'Certain',
			"firm2": self.player.VarRight == 'NoInfo',
			"firm3": self.player.VarRight == 'Imperfect',
			"firm4": self.player.VarLeft == 'Asym1',
			"firm5": self.player.VarLeft == 'Asym2',
			}

	def before_next_page(self):
		self.player.ImplementSignal()


class posterior(Page):
	form_model = models.Player
	form_fields = ['posterior']

	def vars_for_template(self):
		return {'info_select': Constants.NameDict[self.player.info_select], 'signal_good': self.player.signal_good,
				'previous_belief': self.player.participant.vars['previous_belief']}

	def before_next_page(self):
		self.player.participant.vars['previous_belief'] = self.player.posterior  # CUSTOMIZE THIS


page_sequence = [
	# slider,
	# practice,
	prior,
	#### Non-strategy method
	# info1,
	# info2,
	# info3,
	# info4,
	# info5,
	#### Strategy method
	info_overview,
	CertainNoInfo,
	CertainImperfect,
	ImperfectNoInfo,
	Asym1Asym2,
	VarChoice,
	####
	posterior,
]
