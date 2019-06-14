from material.frontend.views import ModelViewSet

from . import models


class HumanViewSet(ModelViewSet):
    """Human View Set"""

    model = models.Human
