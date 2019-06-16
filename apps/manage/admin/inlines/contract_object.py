from django.contrib import admin

from ...models import ContractObject


__all__ = ['ContractObjectInline']


class ContractObjectInline(admin.TabularInline):
    """ContractObject Inline"""

    model = ContractObject
    extra = 1
    readonly_fields = ('created', 'modified', 'deleted',)
