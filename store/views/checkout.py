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



# utility purpose
def final_bill(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = floor(price - (price * (discount / 100)))
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product
    return total





@login_required(login_url='/login')
def checkout(request):
    # get request
    if request.method == 'GET':
        
        form = CheckForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for item in cart:
            size_str = item.get('size')
            tshirt_id = item.get('tshirt')
            size_obj = SizeVarient.objects.get(size = size_str, tshirt = tshirt_id)
            item['size'] = size_obj
            item['tshirt'] = size_obj.tshirt

        # print(cart)

        return render(request, template_name='store/checkout.html', context={'form':form, 'cart':cart})
    else:
    # post request 
        form = CheckForm(request.POST)
        user = None
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for item in cart:
                size_str = item.get('size')
                tshirt_id = item.get('tshirt')
                size_obj = SizeVarient.objects.get(size = size_str, tshirt = tshirt_id)
                item['size'] = size_obj
                item['tshirt'] = size_obj.tshirt
            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = final_bill(cart)

            print(shipping_address, phone, payment_method, total)
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save() 

            # saving order items
            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                size = c.get('size')
                tshirt = c.get('tshirt')
                order_item.price = floor(size.price - (size.price * (tshirt.discount / 100)))
                order_item.quantity = c.get('quantity')
                order_item.size = size
                order_item.tshirt = tshirt
                order_item.save()


            # creating payment
            responce = API.payment_request_create(
            amount = order.total,
            purpose = "Payment for Tshirts",
            send_email = True,
            buyer_name = f'{user.first_name} {user.last_name}',
            email = user.email,
            redirect_url = "http://localhost:8000/validate_payment"
            )

            print(responce['payment_request'])
            payment_request_id = responce['payment_request']['id']
            url = responce['payment_request']['longurl']

            payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_request_id
            payment.save()

            return redirect(url)
            # return redirect('/checkout')
        else:
            return redirect('/checkout')

