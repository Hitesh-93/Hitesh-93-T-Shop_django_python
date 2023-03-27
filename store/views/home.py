from django.shortcuts import render, HttpResponse,redirect
from store.models import Tshirt, SizeVarient, Cart, Order, OrderItem, Payment, Occasion,Brand,Color,IdealFor,NeckType,Sleev
from django.core.paginator import Paginator
from urllib.parse import urlencode


def home(request):

    query = request.GET
    tshirts = []
    tshirts = Tshirt.objects.all()
    
    idelfor = query.get('idelfor')
    brand = query.get('brand')
    color = query.get('color')
    occasion = query.get('occasion')
    sleeve = query.get('sleeve')
    necktype = query.get('necktype')
    page = query.get('page')


    if(page is None or page == ''):
        page = 1


    if idelfor !='' and idelfor is not None:
        tshirts = tshirts.filter(ideal_for__slug = idelfor)
    if brand !='' and brand is not None:
        tshirts = tshirts.filter(brand__slug = brand)
    if color !='' and color is not None:
        tshirts = tshirts.filter(color__slug = color)
    if occasion !='' and occasion is not None:
        tshirts = tshirts.filter(occasion__slug = occasion)
    if sleeve !='' and sleeve is not None:
        tshirts = tshirts.filter(sleev__slug = sleeve)
    if necktype !='' and necktype is not None:
        tshirts = tshirts.filter(neck_type__slug = necktype)
    
    

    brands = Brand.objects.all()
    idealFor = IdealFor.objects.all()
    colors = Color.objects.all()
    occasins = Occasion.objects.all()
    sleeves = Sleev.objects.all()
    neckTypes = NeckType.objects.all()

    cart = request.session.get('cart')
    # tshirts = Tshirt.objects.all()

    paginator = Paginator(tshirts, 6)
    page_obj = paginator.get_page(page)


    query = request.GET.copy()
    query['page'] = ''
    page_url = urlencode(query)

        
    context={
        "page_obj":page_obj,
        # "tshirts":tshirts,
        "brands":brands,
        "idealFor":idealFor,
        "colors":colors,
        "occasions":occasins,
        "sleeves":sleeves,
        "neckTypes":neckTypes,
        'page_url':page_url
    }
    return render(request, template_name='store/home.html', context=context)
