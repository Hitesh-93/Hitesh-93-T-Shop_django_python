from django.shortcuts import render, HttpResponse,redirect
# from store.forms.authforms import CustomerCreationForm, CustomerLoginForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import authenticate,login as loginUser,logout as lgout
from store.models import Tshirt, SizeVarient, Cart, Order, OrderItem, Payment, Occasion,Brand,Color,IdealFor,NeckType,Sleev
from django.views.generic.list import ListView





class OrderListView(ListView):
    model = Order
    template_name='store/orders.html'
    paginate_by = 5
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return  Order.objects.filter(user = user).order_by('-date').exclude(order_status = 'PENDING')