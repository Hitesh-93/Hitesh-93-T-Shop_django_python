from django.contrib import admin
from django.urls import path

from store.views import home,cart,orders,login,signup,logout,show_product,add_to_cart,checkout
from store.views import validatePayment

urlpatterns = [

    path('', home, name='homepage'),
    path('cart/', cart),
    path('orders/', orders, name='orders'),
    path('login/', login),
    path('signup/', signup),
    path('logout/', logout),
    path('product/<str:slug>', show_product),
    path('addtocart/<str:slug>/<str:size>', add_to_cart),
    path('checkout/', checkout),
    path('validate_payment/', validatePayment),

]
