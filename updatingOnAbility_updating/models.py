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
	#### Non-strategy method:
	# num_rounds = 4
	#### Strategy method:
	num_rounds = 1

	# Here I define the state space
	quantile = 0.5
	percentile = int(quantile * 100)

	# Here I define the different information structures:

	AccGood = {'Certain':1, 'Imperfect':0.9, 'NoInfo': 0.5, 'Asym1': 0.9, 'Asym2': 0.7}   # Prob(good signal|top)
	AccBad = {'Certain':1, 'Imperfect':0.9, 'NoInfo': 0.5, 'Asym1': 0.7, 'Asym2': 0.9}   # Prob(bad signal|bottom)

	# Next I define what these will be called in the templates
	NameDict = {"Certain": "Fully informative urns", "Imperfect": "Partially informative urns", "NoInfo": "Uninformative urns", "Asym1": "Positively Skewed urns", "Asym2": "Negatively Skewed urns"}

	# Here i choose the range for elicitation:
	maxUpper = 2
	fineUpper = 0.75
	maxLower = -maxUpper  ## YC's comment: might be good to make price always positive. I feel it easier to think about.
	fineLower = -fineUpper
	steps = 11
	steps2 = 6
	stepsize = (maxUpper - fineUpper)/(steps2 - 1)
	rangeOverFine = np.linspace(fineLower, fineUpper, steps, endpoint = True)
	rangeRoughLower = np.linspace(maxLower, fineLower - stepsize, (steps2-1), endpoint = True)
	rangeRoughUpper = np.linspace(fineUpper + stepsize, maxUpper, (steps2-1), endpoint = True)
	rangeOver = np.concatenate((rangeRoughLower, rangeOverFine, rangeRoughUpper))
	right_side_amounts = []
	for k in range(len(rangeOver)):
		right_side_amounts.append(c(rangeOver[k]))

	# Here I set the probs of implementing each comparision between info structures
	probInfo = [.1, .2, .2, .3, .2]


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	# trial = models.FloatField()

	#### Update
	prior = models.PositiveIntegerField(min=0, max=100)
	info_select = models.CharField()
	signal_good = models.BooleanField()
	## posterior: Non-strategy method
	posterior = models.PositiveIntegerField(min=0, max=100)
	## posteriors: Strategy method
	Imperfect_good = models.PositiveIntegerField(min=0, max=100)
	Imperfect_bad = models.PositiveIntegerField(min=0, max=100)
	Asym1_good = models.PositiveIntegerField(min=0, max=100)
	Asym1_bad = models.PositiveIntegerField(min=0, max=100)
	Asym2_good = models.PositiveIntegerField(min=0, max=100)
	Asym2_bad= models.PositiveIntegerField(min=0, max=100)

	#### Demand for	info structures:

	# Here, I make four pairwise comparison choice variables that capture the elicited willingness to pay that will always be displayed
	CertainVSNoInfo    = models.CurrencyField()
	CertainVSImperfect = models.CurrencyField()
	ImperfectVSNoInfo  = models.CurrencyField()
	Asym1VSAsym2       = models.CurrencyField()
	
	# Next, the variable choice
	VarLeft = models.CharField()
	VarRight = models.CharField()
	VarChoice = models.CurrencyField()

	# these work as follows: random Value between maxLower and maxUpper. If Value is above choice of player, implement RightHandSide info structure and give player +Value payoff. 
	# Otherwise give player LHS info structure and no change to payment. Lottery is between LHS and RHS+PaymentAmount
	# ie: default is LHS, payment/deduction is to get/avoid RHS.
	intransitive = models.BooleanField()

	def VariableChoiceChooser(self, CertainVSNoInfo, CertainVSImperfect, ImperfectVSNoInfo, Asym1VSAsym2):
		if Asym1VSAsym2 > c(0): # then Asym1 is preferred over Asym2
			max1 = "Asym1"
		elif Asym1VSAsym2 < c(0): 
			max1 = "Asym1"
		else: 
			max1 = random.choice(["Asym1", "Asym2"])

		
		A = ( (False, CertainVSNoInfo >= 0, CertainVSImperfect >= 0), (CertainVSNoInfo  <= 0, False, ImperfectVSNoInfo <= 0), (CertainVSImperfect <= 0, ImperfectVSNoInfo >= 0, False))
		A = np.array(A)
		matrix = np.dot(A,np.dot(A,A))
	
	# first check if garp violation
		if np.all(matrix == [[True, False, False], [False, True, False],[False, False, True]]):
			self.intransitive = 1
			max2 =  random.choice(["Certain", "Imperfect", "NoInfo"])
	# if not find second element
		else:
			self.intransitive = 0
			if np.all(A[0] == [False, True, True]):
				max2 = "Certain"
			elif np.all(A[1] == [True, False, True]):
				max2 = "NoInfo"
			else:
				max2 = "Imperfect"
	# record the LHS and RHS of the variable choice
		self.VarLeft = max1
		self.VarRight = max2


	def ImplementSignal(self):
		## COMMENT THIS OUT WHEN TEST IS READY!!!
		self.participant.vars['math_top'] = np.random.binomial(1,0.5)
		#########################################

		info_left = ['Certain', 'Certain', 'Imperfect', 'Asym1', self.VarLeft]
		info_right = ['NoInfo', 'Imperfect', 'NoInfo', 'Asym2', self.VarRight]
		comparisons = [self.CertainVSNoInfo, self.CertainVSImperfect, self.ImperfectVSNoInfo, self.Asym1VSAsym2, self.VarChoice]
		comp_select = random.randrange(len(comparisons))  # randomly select one comparison
		randomprice = random.choice(Constants.right_side_amounts)  # randomly select a price to determine which info structure to implement
		if comparisons[comp_select] > randomprice:
			self.info_select = info_right[comp_select]
			# self.participant.vars['bonus'] += randomprice
		else:
			self.info_select = info_left[comp_select]
		if self.participant.vars['math_top'] == True:    #### NEED TO CUSTOMIZE THIS
			self.signal_good = np.random.binomial(1,Constants.AccGood[self.info_select])
		else:
			self.signal_good = np.random.binomial(1, 1-Constants.AccBad[self.info_select])

