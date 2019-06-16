from django.contrib import admin

from ...models import ObjectProgress


__all__ = ['ObjectProgressInline']


class ObjectProgressInline(admin.TabularInline):
    """ObjectProgress Inline"""

    model = ObjectProgress
    extra = 1
    readonly_fields = ('created', 'modified', 'deleted',)
