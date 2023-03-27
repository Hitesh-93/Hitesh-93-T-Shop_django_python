from django.contrib import admin
from store.models import Tshirt, Brand, Color, IdealFor, NeckType, Occasion, Sleev, SizeVarient, Cart, Order, OrderItem, Payment
from django.utils.html import format_html



# Register your models here.

class SizeVarientConfig(admin.TabularInline):
    model=SizeVarient



class OrderItemConfig(admin.TabularInline):
    model=OrderItem
    


#     ------------- Not Working for OrderItem table -------

# class OrderItemConfiguration(admin.ModelAdmin):
#     model = OrderItem
#     list_display = ['order','tshirt','quantity']
#     list_per_page = 10
    



class TshirtConfig(admin.ModelAdmin):
    inlines = [SizeVarientConfig]
    list_display =['name', 'img', 'discount']
    list_editable=['discount']
    sortable_by = ['name']
    list_filter = ['discount']
    list_per_page = 6
    
    def img(self, obj):
        return format_html(f'''
            <a href='{obj.image.url}' target='_blank'><img height='40px' src='{obj.image.url}' /></a>
        ''')    




class CartConfig(admin.ModelAdmin):
    model = Cart

    list_display = ['sizeVarient',  'tshirt', 'user', 'name']
    fieldsets = (
        ("Cart Info" , {"fields":('get_sizeVarient', 'get_tshirt', 'quantity', 'user')}),
    )
    readonly_fields = ('get_sizeVarient', 'get_tshirt', 'quantity', 'user')


    def get_sizeVarient(self, obj):
        return obj.sizeVarient.size

    def get_tshirt(self, obj):
        tshirt = obj.sizeVarient.tshirt
        tshirt_id = tshirt.id
        name = tshirt.name
        return format_html(f'<a href="/admin/store/tshirt/{tshirt_id}/change/" target="_blank">{name}</a>')

    get_tshirt.short_description = "Tshirt"
    get_sizeVarient.short_description = "Size"

    # def size(self, obj):
    #     return obj.sizeVarient.size
    
    def tshirt(self, obj):
        return obj.sizeVarient.tshirt.name
    
    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name
    
    


class OrderConfig(admin.ModelAdmin):
    model = Order
    list_display=['user', 'shipping_address','phone', 'date', 'order_status']
    list_per_page = 10

    fieldsets = (
        ("Order Information", {"fields":('order_status','user','shipping_address','phone','total')}),
        ("Payment Information",{"fields":('payment','payment_method','payment_request_id','payment_id')})
    )
    readonly_fields = ('payment_method','user','total','shipping_address','phone', 'payment', 'payment_request_id','payment_id')

    inlines=[OrderItemConfig]


    # def name(self, obj):
    #     return obj.user.first_name + ' ' + obj.user.last_name

    def payment(self, obj):
        payment_id =  obj.payment_set.all()[0].id
        return format_html(f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank">Click for payment info</a>')

    def payment_request_id(self, obj):
        return obj.payment_set.all()[0].payment_request_id
    
    def payment_id(self, obj):
        payment_id = obj.payment_set.all()[0].payment_id
        if(payment_id is None or payment_id == ''):
            return "Payment Id not available"
        else:
            return payment_id
    


admin.site.register(Tshirt, TshirtConfig )
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(IdealFor)
admin.site.register(NeckType)
admin.site.register(Occasion)
admin.site.register(Sleev)
admin.site.register(Cart, CartConfig)
admin.site.register(Order, OrderConfig)
admin.site.register(OrderItem)
admin.site.register(Payment)
