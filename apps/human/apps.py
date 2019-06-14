from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class HumanConfig(ModuleMixin, AppConfig):
    """Human App Config"""

    name = 'apps.human'
    label = 'human'
    icon = '<i class="material-icons">settings_applications</i>'
