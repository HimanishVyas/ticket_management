from django.apps import apps
from django.contrib import admin
from apps.ticket.models import Item, ItemSpare, CustomerWiseItem, ItemProblemType

models = apps.get_app_config("ticket").get_models()
for model in models:
    admin.site.register(model)

admin.site.unregister(Item)
admin.site.unregister(ItemSpare)
admin.site.unregister(CustomerWiseItem)
admin.site.unregister(ItemProblemType)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['ItemName']


@admin.register(ItemSpare)
class ItemSpareAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']


@admin.register(CustomerWiseItem)
class CustomerWiseItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']


@admin.register(ItemProblemType)
class ItemProblemTypeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['item']
