from django.contrib import admin
from django.urls import path

from store.views import home,cart,add_to_cart,checkout,ProductDetailView
from store.views import LoginView,signup,logout
from store.views import OrderListView
from store.views import validatePayment
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('', home, name='homepage'),
    path('cart/', cart),
    path('orders/', login_required(OrderListView.as_view(), login_url='/login/') , name='orders'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', signup),
    path('logout/', logout),
    path('product/<str:slug>', ProductDetailView.as_view()),
    path('addtocart/<str:slug>/<str:size>', add_to_cart),
    path('checkout/', checkout),
    path('validate_payment/', validatePayment),
]
