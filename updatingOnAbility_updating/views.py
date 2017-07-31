from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class info1(Page):
	form_model = models.Player
	form_fields = ['attentioncheck']

class info2(Page):
	form_model = models.Player
	form_fields = ['attentioncheck']


page_sequence = [
	info1,
	info2,
]
