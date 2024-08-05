from django.shortcuts import render, reverse

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from users.models import User
from customer.models import Customer, Cart, OfferCupen, BillDetails

from web.models import RestorantCategory, Restorant, Slide, Foodcategory, Fooditem
from customer.models import Cart

from django.contrib.auth.decorators import login_required
from django.db.models import Sum







@login_required(login_url='web:login')  # Ensure only logged-in users can access the index view
def index(request):
    restorant_categorys = RestorantCategory.objects.all()
    restorants = Restorant.objects.all()
    
    foodcategories = Foodcategory.objects.all()
    fooditems = Fooditem.objects.all()

    slides = Slide.objects.all()

    context = {
        "restorant_categorys": restorant_categorys,
        "restorants": restorants,
        "slides": slides,
        'foodcategories': foodcategories,
        'fooditems': fooditems
    }
    return render(request, 'web/index.html', context=context)




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            context = {
                "error" : True,
                "message" : "Invalid email or pasword"
            }
            return render(request, 'web/login.html', context=context)
    else:
        return render(request, 'web/login.html')
    
    

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {
                "error" : True,
                "message" : "Email already registered"
            }
            return render(request, 'web/register.html', context=context)
        else:
            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_customer=True
            )

            user.save()

            customer = Customer.objects.create(
                user=user,
            )

            customer.save()
            return HttpResponseRedirect(reverse('web:login'))

    else:
        return render(request, 'web/register.html')
    

def logout(request):
    user = request.user
    auth_logout(request)

    return HttpResponseRedirect(reverse('web:login'))





@login_required(login_url='web:login')
def singlerest(request, id):
    user=request.user
    customer=Customer.objects.get(user=user)
    singlerest = Restorant.objects.get(id=id)
    foodcategories = Foodcategory.objects.filter(restorant=singlerest)
    fooditems = Fooditem.objects.filter(restorant=singlerest, foodcategory__in=foodcategories)
    carts_count = Cart.objects.filter(restorant=singlerest, customer=customer).count()
   
    carts = Cart.objects.filter(restorant=singlerest, customer=customer)
    cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum']

    cart_quantities = {cart.product: cart.quantity for cart in carts}
    prod_with_qty = [(fooditem, cart_quantities.get(fooditem, 0)) for fooditem in fooditems]



    context = {
            "singlerest": singlerest,
            'foodcategories': foodcategories,
            'fooditems': fooditems,
            'prod_with_qty': prod_with_qty,
            'cart_amount': cart_amount,
            'carts_count': carts_count
            
    }
    return render(request, 'web/singlerest.html', context=context)







@login_required(login_url='web:login')
def restorant(request, id):
    restorant_categorys = RestorantCategory.objects.all()
    category = RestorantCategory.objects.get(id=id)
    restorants = Restorant.objects.filter(category=category)

    context = {
            "category": category,
            "restorant_categorys": restorant_categorys,
            "restorants": restorants
    }
    return render(request, 'web/restorant.html', context=context)



def add_cart(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    product = Fooditem.objects.get(id=id)
    singlerest = product.restorant 

    previous = None

    if Cart.objects.filter(customer=customer).exists():
        previous = Cart.objects.filter(customer=customer).last()

    if previous:
        cart_store = previous.restorant
        if cart_store == singlerest:
            cart = Cart.objects.create(
                customer=customer,
                product=product,
                amouunt=product.price,
                restorant=singlerest,
                quantity=1
            )
        else:
            cart_items = Cart.objects.filter(customer=customer)
            for item in cart_items:
                item.delete()

            cart = Cart.objects.create(
                customer=customer,
                product=product,
                amouunt=product.price,
                restorant=singlerest,
                quantity=1
            )
    else:
        cart = Cart.objects.create(
            product=product,
            customer=customer,
            amouunt=product.price,
            quantity=1,
            restorant=singlerest
        )
    
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

   

def cart_plus(request, id):
    user=request.user
    customer=Customer.objects.get(user=user)
    product = Fooditem.objects.get(id=id)
    cart = Cart.objects.get(product=product, customer=customer)

    cart.quantity += 1
    cart.amouunt += product.price

    cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_minus(request, id):
    user=request.user
    product = Fooditem.objects.get(id=id)
    customer=Customer.objects.get(user=user)
    cart = Cart.objects.get(product=product, customer=customer)

    cart.quantity -= 1
    cart.amouunt -= product.price

    cart.save()

    if cart.quantity == 0:
        cart.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_total(request, id):
    user=request.user
    product = Fooditem.objects.get(id=id)
    customer=Customer.objects.get(user=user)
    cart = Cart.objects.get(product=product, customer=customer)

    
    cart_total=cart.product*cart.quantity

    cart_total.save()

    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))









def cart(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum']
    item_total = cart_amount
    delivery_charges = 50
    offer_applied = 30
    offer = int(offer_applied * cart_amount / 100)
    final_amount = int(item_total - offer + delivery_charges)
    if carts.exists():
        restorant = carts.first().restorant
    else:
        restorant = None


    cart_single = carts.last()

    singlerest = cart_single.restorant
    

    context = {
            "restorant": restorant,
            "carts": carts,
            "singlerest": singlerest,
            "cart_amount": cart_amount,
            "offer_applied": offer_applied,
            "delivery_charges": delivery_charges,
            "final_amount": final_amount,
            "offer": offer
    }
    return render(request, 'web/cart.html', context=context)






@login_required(login_url='web:login')
def checkout(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum']
    item_total = cart_amount
    delivery_charges = 50
    offer_applied = 30
    restorants = Restorant.objects.all()
    offer = int(offer_applied * cart_amount / 100)
    final_amount = int(item_total - offer_applied * cart_amount / 100 + delivery_charges)

    context = {
            "restorants": restorants,
            "carts": carts,
            "cart_amount": cart_amount,
            "offer_applied": offer_applied,
            "delivery_charges": delivery_charges,
            "final_amount": final_amount,
            "offer": offer
    }
    return render(request, 'web/checkout.html', context=context)




@login_required(login_url='web:login')
def offers(request):
    restorants = Restorant.objects.all()
    offer_cupen = OfferCupen.objects.all()

    context = {
            "restorants": restorants,
            "offer_cupen": offer_cupen
    }
    return render(request, 'web/offers.html', context=context)



@login_required(login_url='web:login')
def account(request):
    # singlerest = Restorant.objects.get(id=id)
    restorants = Restorant.objects.all()
    # singlerests = Restorant.objects.all()[:5]flightradar olx india canava  home workout telegram calculator blockudoku score hero mini miltia

    context = {
            # "singlerest": singlerest,
            "restorants": restorants
    }
    return render(request, 'web/account.html', context=context)
















# from django.shortcuts import render, reverse
# from django.http import HttpResponseRedirect
# from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from django.contrib.auth.decorators import login_required

# from users.models import User
# from customer.models import Customer

# @login_required(login_url='web:login')  # Ensure only logged-in users can access the index view
# def index(request):
    # restorant_categorys = RestorantCategory.objects.all()
    # restorants = Restorant.objects.all()

    # slides = Slide.objects.all()

    # context = {
    #     "restorant_categorys": restorant_categorys,
    #     "restorants": restorants,
    #     "slides": slides
    # }
    # return render(request, 'web/index.html', context=context)

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             auth_login(request, user)
#             return HttpResponseRedirect(reverse('web:index'))
#         else:
#             context = {
#                 "error": True,
#                 "message": "Invalid email or password"
#             }
#             return render(request, 'web/login.html', context=context)
#     else:
#         return render(request, 'web/login.html')

# def register(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password')

#         if User.objects.filter(email=email).exists():
#             context = {
#                 "error": True,
#                 "message": "Email already registered"
#             }
#             return render(request, 'web/register.html', context=context)
#         else:
#             user = User.objects.create_user(
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 password=password,
#                 is_customer=True
#             )

#             user.save()

#             customer = Customer.objects.create(
#                 user=user,
#             )

#             customer.save()
#             return HttpResponseRedirect(reverse('web:login'))

#     else:
#         return render(request, 'web/register.html')

# def logout(request):
#     user = request.user
#     auth_logout(request)
#     return HttpResponseRedirect(reverse('web:login'))
