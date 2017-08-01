from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np

class info1(Page):
	form_model = models.Player
	form_fields = ['CertainVSNoInfo']
	def vars_for_template(self):
		rangeOver = np.concatenate((Constants.rangeRoughLower,Constants.rangeOverFine,Constants.rangeRoughUpper))
		right_side_amounts =[c(rangeOver[k]) for k in range(len(rangeOver))]
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["NoInfo"], "right_side_amounts": right_side_amounts}	

class info2(Page):
	form_model = models.Player
	form_fields = ['CertainVSImperfect']
	def vars_for_template(self):
		rangeOver = np.concatenate((Constants.rangeRoughLower,Constants.rangeOverFine,Constants.rangeRoughUpper))
		right_side_amounts =[c(rangeOver[k]) for k in range(len(rangeOver))]
		return {"left_side": Constants.NameDict["Certain"], "right_side": Constants.NameDict["Imperfect"], "right_side_amounts": right_side_amounts}	

class info3(Page):
	form_model = models.Player
	form_fields = ['ImperfectVSNoInfo']
	def vars_for_template(self):
		rangeOver = np.concatenate((Constants.rangeRoughLower,Constants.rangeOverFine,Constants.rangeRoughUpper))
		right_side_amounts =[c(rangeOver[k]) for k in range(len(rangeOver))]
		return {"left_side": Constants.NameDict["Imperfect"], "right_side": Constants.NameDict["NoInfo"], "right_side_amounts": right_side_amounts}	

class info4(Page):
	form_model = models.Player
	form_fields = ['Asym1VSAsym2']
	def vars_for_template(self):
		rangeOver = np.concatenate((Constants.rangeRoughLower,Constants.rangeOverFine,Constants.rangeRoughUpper))
		right_side_amounts =[c(rangeOver[k]) for k in range(len(rangeOver))]
		return {"left_side": Constants.NameDict["Asym1"], "right_side": Constants.NameDict["Asym2"], "right_side_amounts": right_side_amounts}	

class info5(Page):
	form_model = models.Player
	form_fields = ['VarChoice']
	def vars_for_template(self):
		rangeOver = np.concatenate((Constants.rangeRoughLower,Constants.rangeOverFine,Constants.rangeRoughUpper))
		right_side_amounts =[c(rangeOver[k]) for k in range(len(rangeOver))]
		max1, max2, intransitive = self.player.VariableChoiceChooser(self.player.CertainVSNoInfo, self.player.CertainVSImperfect, self.player.ImperfectVSNoInfo, self.player.Asym1VSAsym2)	
		return {"left_side": Constants.NameDict(max1), "right_side": Constants.NameDict(max2), "right_side_amounts": right_side_amounts}	

page_sequence = [
	info1,
	info2,
	info3,
	info4,
	info5,
]

