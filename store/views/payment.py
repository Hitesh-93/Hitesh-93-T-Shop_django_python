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




def validatePayment(request):

    user = None
    if request.user.is_authenticated:
        user = request.user

    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    print(payment_request_id, payment_id)
    response = API.payment_request_payment_status(payment_request_id, payment_id)
    status = response.get('payment_request').get('payment').get('status')
    
    if status != 'Failed':
        print('Payment Success')
        try:
            payment = Payment.objects.get(payment_request_id = payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = "PLACED"
            order.save()

            cart = []
            request.session['cart'] = cart
            Cart.objects.filter(user = user).delete()

            return redirect('orders')

        except:
            return render(request, template_name='store/payment_failed.html')
        
    else:
        return render(request, template_name='store/payment_failed.html')
    