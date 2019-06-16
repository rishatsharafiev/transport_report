from django.contrib import admin


class ZoneAdmin(admin.ModelAdmin):
    """Zone Admin"""
    list_per_page = 20

    list_display = ('id', 'name', 'parent', 'zonetype', 'address',)
    list_filter = ('name', 'parent', 'zonetype', 'address',)
    search_fields = ('name', 'parent__name',)