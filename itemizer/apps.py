from django.apps import AppConfig
from irs.models import F8872
from watson import search as watson

class ItemizerConfig(AppConfig):
    name = "itemizer"
    def ready(self):
        watson.register(F8872)