from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class welcome(Page):
	pass

class IRB(Page):
	pass


page_sequence = [
	welcome,
	IRB,
]
