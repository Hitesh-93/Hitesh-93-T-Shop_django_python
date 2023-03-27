from django.shortcuts import render, HttpResponse,redirect
from store.forms.authforms import CustomerCreationForm, CustomerLoginForm
from django.contrib.auth import authenticate,login as loginUser,logout as lgout
from store.models import Tshirt, SizeVarient, Cart, Order, OrderItem, Payment, Occasion,Brand,Color,IdealFor,NeckType,Sleev
from store.forms.checkout_form import CheckForm
from django.views.generic.base import View



class LoginView(View):
    def get(self, request):
        form = CustomerLoginForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        return render(request, template_name='store/login.html',  context={"form":form})
    

    def post(self, request):
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
            return redirect('login')
        context = {
            "form":form
        }
        return render(request, template_name='store/signup.html',context=context)





def logout(request):
    # request.session.clear()
    lgout(request)
    return render(request, template_name='store/home.html')
    
