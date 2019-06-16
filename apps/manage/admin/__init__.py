"""Admin"""

from django.contrib import admin

from .contractor import ContractorAdmin
from .zone_type import ZoneTypeAdmin
from .zone import ZoneAdmin
from .contract import ContractAdmin
from .contract_object import ContractObjectAdmin
from .object_progress import ObjectProgressAdmin

from ..models import *

admin.site.register(Contractor, ContractorAdmin)
admin.site.register(ZoneType, ZoneTypeAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractObject, ContractObjectAdmin)
admin.site.register(ObjectProgress, ObjectProgressAdmin)

admin.site.site_header = 'DREAMROAD'
admin.site.site_title = 'DREAMROAD'
admin.site.index_title = 'Панель управления'
