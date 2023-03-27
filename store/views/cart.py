from django.shortcuts import render, HttpResponse,redirect
from store.forms.authforms import CustomerCreationForm, CustomerLoginForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as loginUser,logout as lgout
from store.models import Tshirt, SizeVarient, Cart, Order, OrderItem, Payment, Occasion,Brand,Color,IdealFor,NeckType,Sleev
from django.db.models import Min
from math import floor
from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckForm
from instamojo_wrapper import Instamojo

from Tshop.settings import API_KEY, AUTH_TOKEN

API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')




def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    
    for item in cart:
        tshirt_id = item.get('tshirt')
        tshirt = Tshirt.objects.get(id = tshirt_id)
        item['size'] = SizeVarient.objects.get(tshirt = tshirt_id, size = item['size'])
        item['tshirt'] = tshirt

        print(cart)
    return render(request, template_name='store/cart.html', context={'cart' : cart})




def add_to_cart(request, slug, size):
    user = None
    if request.user.is_authenticated:
        user = request.user

    cart = request.session.get('cart')
    # size_temp = size
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug = slug)
    add_cart_for_anom_user(cart, size, tshirt)
    

    if user is not None:
        add_cart_to_database(user, size, tshirt)

    request.session['cart'] = cart
    # print(cart)
    return_url = request.GET.get('return_url')
    return redirect(return_url)




def add_cart_to_database(user, size, tshirt):
    size = SizeVarient.objects.get(size = size, tshirt = tshirt)
    existing = Cart.objects.filter(user = user, sizeVarient = size)

    if len(existing) > 0:
        obj = existing[0]
        obj.quantity = obj.quantity + 1
        obj.save()

    else: 
        c = Cart()
        c.user = user
        c.sizeVarient = size
        c.quantity = 1
        c.save()




def add_cart_for_anom_user(cart, size, tshirt):
    flag = True

    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')
        size_obj = cart_obj.get('size')
        if t_id==tshirt.id and size==size_obj:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity']+1

    if flag:
        cart_obj = {
            'tshirt' : tshirt.id,
            'size' : size,
            'quantity' : 1
        }
        cart.append(cart_obj)
