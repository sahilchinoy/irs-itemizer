from django.apps import AppConfig
from irs.models import F8872
import watson

class ItemizerConfig(AppConfig):
    name = "itemizer"
    def ready(self):
        watson.register(F8872)