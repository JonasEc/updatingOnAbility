from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)


author = 'Jonas Mueller Gastell & Yucheng Liang'

doc = """
Experiment to Test Updating on Ability
"""


class Constants(BaseConstants):
	name_in_url = 'experiment'
	players_per_group = None
	num_rounds = 1
	test = "test"


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	pass
