from django.shortcuts import render, HttpResponse,redirect
from store.models import Tshirt, SizeVarient, Cart, Order, OrderItem, Payment, Occasion,Brand,Color,IdealFor,NeckType,Sleev
from math import floor
from django.views.generic.detail import DetailView




class ProductDetailView(DetailView):
    template_name='store/product_details.html'
    model = Tshirt
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        # slug = kwargs.get('slug')
        tshirt = context.get('tshirt')
        request = self.request
        # tshirt = Tshirt.objects.get(slug=slug)
        size = request.GET.get('size')

        if size is None:
            size  = tshirt.sizevarient_set.all().order_by('price').first()
        else:
            size  = tshirt.sizevarient_set.get(size = size)

        size_price  = floor(size.price)
        sell_price  = size_price - (size_price * (tshirt.discount / 100))
        sell_price = floor(sell_price)
        
        context={'tshirt':tshirt, 'price':size_price, 'sell_price':sell_price, 'active_size': size }
       
        return context

