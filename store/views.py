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

 
# Create your views here.

def show_product(request, slug):
    tshirt = Tshirt.objects.get(slug=slug)
    size = request.GET.get('size')

    if size is None:
        size  = tshirt.sizevarient_set.all().order_by('price').first()
    else:
        size  = tshirt.sizevarient_set.get(size = size)

    size_price  = floor(size.price)
    sell_price  = size_price - (size_price * (tshirt.discount / 100))
    sell_price = floor(sell_price)
    
    context={'tshirt':tshirt, 'price':size_price, 'sell_price':sell_price, 'active_size': size }

    return render(request, template_name='store/product_details.html', context=context )
   




def home(request):

    brands = Brand.objects.all()
    idealFor = IdealFor.objects.all()
    colors = Color.objects.all()
    occasins = Occasion.objects.all()
    sleeves = Sleev.objects.all()
    neckTypes = NeckType.objects.all()

    tshirts = Tshirt.objects.all()
        
    context={
        "tshirts":tshirts,
        "brands":brands,
        "idealFor":idealFor,
        "colors":colors,
        "occasions":occasins,
        "sleeves":sleeves,
        "neckTypes":neckTypes
    }
    return render(request, template_name='store/home.html', context=context)





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





@login_required(login_url='/login')
def orders(request):
    user = request.user
    orders = Order.objects.filter(user = user).order_by('-date').exclude(order_status = 'PENDING')
    context={
        'orders':orders
    }
    return render(request, template_name='store/orders.html', context=context)





def login(request):
    if request.method=='GET':
        form = CustomerLoginForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page

        return render(request, template_name='store/login.html',  context={"form":form})
    
    else:
        form=CustomerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)

            if user:
                loginUser(request, user)

                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizeVarient = SizeVarient.objects.get(size = size, tshirt = tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                cart = Cart.objects.filter(user = user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size' : c.sizeVarient.size,
                        'tshirt' : c.sizeVarient.tshirt.id,
                        'quantity' : c.quantity
                    }
                    session_cart.append(obj)
                
                request.session['cart'] = session_cart

                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = "homepage"
                return redirect(next_page)
        else:
           return render(request, template_name='store/login.html', context={"form":form})





def signup(request):
    if(request.method =='GET'):
        form=CustomerCreationForm()
        context={
            "form":form
        }
        return render(request, template_name='store/signup.html',context=context)

    else:
        form=CustomerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            print(user)
            user.email = user.username
            user.save()
            return render(request, template_name='store/login.html')
        context = {
            "form":form
        }
        return render(request, template_name='store/signup.html',context=context)





def logout(request):
    # request.session.clear()
    lgout(request)
    return render(request, template_name='store/home.html')
    




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