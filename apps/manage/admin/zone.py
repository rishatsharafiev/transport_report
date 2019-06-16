from django.contrib import admin


class ZoneAdmin(admin.ModelAdmin):
    """Zone Admin"""
    list_per_page = 20

    # list_display = ('id', 'guid', 'name', 'parent', 'updated_at',
    #                 'get_retail_min_margin', 'get_retail_max_margin', 'get_retail_drop_margin',
    #                 'get_special_max_margin',
    #                 'get_online_min_margin', 'get_online_max_margin', 'get_online_drop_margin',
    #                 'transport_price',)
    # list_filter = ('is_available',)
    #
    # search_fields = ('name',)
    # readonly_fields = ('created_at', 'updated_at',)
