from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

import numpy as np

author = 'Jonas Mueller Gastell & Yucheng Liang'

doc = """
Experiment to Test Updating on Ability
"""


class Constants(BaseConstants):
	name_in_url = 'experiment2'
	players_per_group = None
	num_rounds = 4

	# Here I define the different information structures:
	# naming convention: AccNameNSignal << Acc for Accuracy, Name for structure name, N for iteration of structure if applicable, Signal for whether good or bad 
	AccAsym1Good = 0.85 # if in upper half, get good signal with AccAsym1Good % probability
	AccAsym1Bad = 0.6 # if in lower half, get bad signal with AccAsym1Bad % probability

	AccAsym2Good = AccAsym1Bad # the other info structure is a mirror image of the first
	AccAsym2Bad = AccAsym1Good

	AccImpGood = 0.85
	AccImpBad = 0.85

	# no info: 0.5 for both; full info: 1 for both

	# Next I define what these will be called in the templates
	NameDict = {"Certain": "Fully informative urns", "Imperfect": "Partially informative urns", "NoInfo": "Uninformative urns", "Asym1": "Positively Skewed urns", "Asym2": "Negatively Skewed urns"}

	# Here i choose the range for elicitation:
	maxUpper = 2
	fineUpper = 0.75
	maxLower = -maxUpper
	fineLower = -fineUpper
	steps = 11
	steps2 = 6
	stepsize = (maxUpper - fineUpper)/(steps2 - 1)
	rangeOverFine = np.linspace(fineLower, fineUpper, steps, endpoint = True)
	rangeRoughLower = np.linspace(maxLower, fineLower - stepsize, (steps2-1), endpoint = True)
	rangeRoughUpper = np.linspace(fineUpper + stepsize, maxUpper, (steps2-1), endpoint = True)



class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	
	#### Demand for	:

	# Here, I make four pairwise comparison choice variables that capture the elicited willingness to pay that will always be displayed
	CertainVSNoInfo    = models.CurrencyField()
	CertainVSImperfect = models.CurrencyField()
	ImperfectVSNoInfo  = models.CurrencyField()
	Asym1VSAsym2       = models.CurrencyField()
	
	# Next, the variable choice
	VarChoice = models.CurrencyField()


	# Next, I make the four possible choices, one of which will be displayed
	# CertainVSAsym1   = models.CurrencyField()
	# ImperfectVSAsym1 = models.CurrencyField()
	# NoInfoVSAsym1    = models.CurrencyField()
	# CertainVSAsym2   = models.CurrencyField()
	# ImperfectVSAsym2 = models.CurrencyField()
	# NoInfoVSAsym2    = models.CurrencyField()	


	# these work as follows: random Value between maxLower and maxUpper. If Value is above choice of player, implement RightHandSide info structure and give player +Value payoff. 
	# Otherwise give player LHS info structure and no change to payment. Lottery is between LHS and RHS+PaymentAmount
	# ie: default is LHS, payment/deduction is to get/avoid RHS.
	intransitiveChoice = models.BooleanField()

	def VariableChoiceChooser(CertainVSNoInfo, CertainVSImperfect, ImperfectVSNoInfo, Asym1VSAsym2):
		if Asym1VSAsym2 > c(0): # then Asym1 is preferred over Asym2
			max1 = "Asym2"
		elif Asym1VSAsym2 < c(0): 
			max1 = "Asym1"
		else: 
			max1 = random.choice(["Asym1", "Asym2"])

		
		A = ( (False, CertainVSNoInfo >= 0, CertainVSImperfect >= 0), (CertainVSNoInfo  <= 0, False, ImperfectVSNoInfo <= 0), (CertainVSImperfect <= 0, ImperfectVSNoInfo >= 0, False))
		A = np.array(A)
		matrix = np.dot(A,np.dot(A,A))
	
	# first check if garp violation
		if np.all(matrix == [[True, False, False], [False, True, False],[False, False, True]]):
			intransitive = 1
			max2 =  random.choice(["Certain", "Imperfect", "NoInfo"])\
	# if not find second element
		else:
			intransitive = 0
			if np.all(A[1] == [False, True, True]):
				max2 = "Certain"
			elif np.all(A[2] == [True, False, True]):
				max2 = "NoInfo"
			else:
				max2 = "Imperfect"

		return max1, max2, intransitive

			