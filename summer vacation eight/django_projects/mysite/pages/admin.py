from django.contrib import admin
from .models import ShopItem, UserItem


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")


admin.site.register(UserItem)
#
