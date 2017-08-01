from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

import numpy as np

maxUpper = 2
fineUpper = 0.75
maxLower = -maxUpper
fineLower = -fineUpper
steps = 11
steps2 = 6
stepsize = (maxUpper - fineUpper) / (steps2 - 1)
rangeOverFine = np.linspace(fineLower, fineUpper, steps, endpoint=True)
rangeRoughLower = np.linspace(maxLower, fineLower - stepsize, (steps2 - 1), endpoint=True)
rangeRoughUpper = np.linspace(fineUpper + stepsize, maxUpper, (steps2 - 1), endpoint=True)
rangeOver = np.concatenate((rangeRoughLower, rangeOverFine, rangeRoughUpper))
right_side_amounts = [c(rangeOver[k]) for k in range(len(rangeOver))]

print right_side_amounts