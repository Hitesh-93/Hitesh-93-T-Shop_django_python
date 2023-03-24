from django.contrib import admin
from .models import Tshirt, Brand, Color, IdealFor, NeckType, Occasion, Sleev, SizeVarient, Cart, Order, OrderItem, Payment

# Register your models here.

class SizeVarientConfig(admin.TabularInline):
    model=SizeVarient


class TshirtConfig(admin.ModelAdmin):
    inlines = [SizeVarientConfig]
    # list_display =['name', 'slug']
    # list_editable=['slug']
    




admin.site.register(Tshirt, TshirtConfig )
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(IdealFor)
admin.site.register(NeckType)
admin.site.register(Occasion)
admin.site.register(Sleev)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
