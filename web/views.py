from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from users.models import User
from django.contrib.auth.decorators import login_required
from customer.models import *

from web.models import *
from customer.models import Cart

from django.db.models import Sum

from decimal import Decimal  # Import Decimal for precise calculations

from django.shortcuts import redirect
from django.contrib import messages
import random
import string
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

def generate_unique_order_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))





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
        if cart_store != singlerest:
            # Redirect to confirmation page
            return redirect(reverse('web:confirm_delete_cart', kwargs={'id': id}))
    
    # Proceed to add the item to the cart
    cart = Cart.objects.create(
        customer=customer,
        product=product,
        amouunt=product.price,
        restorant=singlerest,
        quantity=1
    )
    
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





def confirm_delete_cart(request, id):
    return render(request, 'web/confirm_delete_cart.html', {'id': id})


def add_cart_confirm(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    product = Fooditem.objects.get(id=id)
    singlerest = product.restorant

    # Delete all previous cart items from a different store
    Cart.objects.filter(customer=customer).delete()

    # Add the new item to the cart
    Cart.objects.create(
        customer=customer,
        product=product,
        amouunt=product.price,
        restorant=singlerest,
        quantity=1
    )

    return HttpResponseRedirect(reverse('web:singlerest id=singlerest.id'))


   

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


def calculate_cart_details(customer):
    carts = Cart.objects.filter(customer=customer)
    cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum'] or 0
    delivery_charges = 50 if carts.exists() else 0
    return cart_amount, delivery_charges


def cart(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    addresses = Address.objects.filter(customer=customer)
    restorant = None
    error_message = ""
    success_message = ""
    selected_address = None

    # Use the helper function
    cart_amount, delivery_charges = calculate_cart_details(customer)

    discount = 0
    if carts.exists():
        restorant = carts.first().restorant

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = OfferCupen.objects.get(offer_code=code)
            if offer.is_percentage:
                discount = (float(offer.offer_amount) / 100) * cart_amount
                discount = round(discount)
            else:
                discount = offer.offer_amount
                success_message = "Coupon applied successfully!"
        except OfferCupen.DoesNotExist:
            error_message = "Invalid coupon code. Please try again."

    to_pay_amount = float(cart_amount) + float(delivery_charges) - float(discount)

    if BillDetails.objects.filter(customer=customer).exists():
        bill_details = BillDetails.objects.get(customer=customer)
        bill_details.item_total = cart_amount
        bill_details.final_amount = cart_amount + delivery_charges - float(bill_details.offer_applied)
        bill_details.save()
        selected_address = bill_details.address
    else:
        bill_details = BillDetails.objects.create(
            customer=customer,
            item_total=cart_amount,
            delivery_charges=delivery_charges,
            final_amount=cart_amount + delivery_charges,
            offer_applied=0
        )

    context = {
        "restorant": restorant,
        "carts": carts,
        "cart_amount": cart_amount,
        "delivery_charges": delivery_charges,
        "bill_details": bill_details,
        "to_pay_amount": to_pay_amount,
        "discount": discount,
        "addresses": addresses,
        "error_message": error_message,
        "success_message": success_message,
        "selected_address": selected_address,
    }
    return render(request, 'web/cart.html', context=context)





def apply_cupon(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    
    # Initialize discount as a Decimal
    discount = Decimal('0.0')
    
    # Fetch all available coupons
    offer_cupens = OfferCupen.objects.all()

    # Calculate cart amount using Decimal
    cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum']
    cart_amount = Decimal(cart_amount) if cart_amount else Decimal('0.0')
    
    # Delivery charges as Decimal
    delivery_charges = Decimal('50.0')

    # If a coupon is being applied
    if request.method == "POST":
        offer_id = request.POST.get('offer_id')

        # Get the coupon by ID
        offer_cupen = get_object_or_404(OfferCupen, id=offer_id)

        # Calculate the discount based on coupon type
        if offer_cupen.is_percentage:
            discount = (offer_cupen.offer_amount / Decimal('100.0')) * cart_amount
        else:
            discount = Decimal(offer_cupen.offer_amount)  # Convert offer amount to Decimal

        # Calculate the total amount to pay
        to_pay_amount = cart_amount + delivery_charges - discount

        # Store a success message and redirect to the offers page
        messages.success(request, "Coupon applied successfully!")
        return redirect('web:offers')

    # Context for rendering the offers page
    context = {
        'offer_cupens': offer_cupens,
        'cart_amount': cart_amount,
        'delivery_charges': delivery_charges,
        'discount': discount,
    }

    return render(request, 'web/offers.html', context)




@login_required(login_url='web:login')
def offers(request):
    restorants = Restorant.objects.all()
    offer_cupens = OfferCupen.objects.all()
    print(offer_cupens)

    context = {
            "restorants": restorants,
            "offer_cupens": offer_cupens
    }
    return render(request, 'web/offers.html', context=context)





@login_required(login_url='web:login')
def add_address(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    if request.method == 'POST':
        address=request.POST.get('address')
        apartment=request.POST.get('apartment')
        landmark=request.POST.get('landmark')
        pin_code=request.POST.get('pin_code')
        mobile_no=request.POST.get('mobile_no')
        address_type=request.POST.get('address_type')


        address = Address.objects.create(
            customer=customer,
            address=address,
            apartment=apartment,
            landmark=landmark,
            pin_code=pin_code,
            mobile_no=mobile_no,
            address_type=address_type
        )
        return HttpResponseRedirect(reverse('web:address'))
    else:
        return render(request, 'web/add_address.html')
    






@login_required(login_url='web:login')
def address(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    addresses = Address.objects.filter(customer=customer)

    context = {
            "addresses": addresses
    }
    return render(request, 'web/address.html', context=context)





@login_required(login_url='web:login')
def delete_address(request, id):
    user = request.user
    try:
        # Get the customer's address
        address = Address.objects.get(id=id, customer__user=user)
        
        # Delete the address
        address.delete()
        messages.success(request, "Address deleted successfully.")
    except Address.DoesNotExist:
        messages.error(request, "Address not found.")
    
    # Redirect back to the previous page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





@login_required(login_url='web:login')
def edit_address(request, id):
    user = request.user
    customer=Customer.objects.get(user=user)
    address_details = Address.objects.get(id=id, customer=customer)

    if request.method == 'POST':
        address=request.POST.get('address')
        apartment=request.POST.get('apartment')
        landmark=request.POST.get('landmark')
        pin_code=request.POST.get('pin_code')
        mobile_no=request.POST.get('mobile_no')
        address_type=request.POST.get('address_type')

        
        address_details.address = address
        address_details.apartment = apartment
        address_details.landmark = landmark
        address_details.pin_code = pin_code
        address_details.mobile_no = mobile_no
        address_details.address_type = address_type
        address_details.save()
        return HttpResponseRedirect(reverse('web:address'))
    else:
        return render(request, 'web/add_address.html', {'address_details': address_details, 'is_edit': True})






@login_required(login_url='web:login')
def set_address(request, id):
    user = request.user
    customer=Customer.objects.get(user=user)
    address = Address.objects.get(id=id)
    cart_bill = BillDetails.objects.get(customer=customer)
    cart_bill.address=address
    cart_bill.save()

    return HttpResponseRedirect(reverse('web:cart'))







@login_required(login_url='web:login')
def checkout(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    
    # Assuming CartItem is the model representing items in the cart, and it's linked to Customer
    cart_items = Cart.objects.filter(customer=customer)

    try:
        cart_bill = BillDetails.objects.get(customer=customer)
    except BillDetails.DoesNotExist:
        cart_bill = None

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        selected_address = cart_bill.address if cart_bill else None

        # Create a new order with the address and order ID
        new_order = Order.objects.create(
            customer=customer,
            item_total=cart_bill.item_total if cart_bill else 0,
            offer=cart_bill.offer_applied if cart_bill else 0,
            delivery=cart_bill.delivery_charges if cart_bill else 0,
            total=cart_bill.final_amount if cart_bill else 0,
            address=selected_address,
            order_id=generate_unique_order_id(),  # Function to generate a unique order ID
            payment_method=payment_method,
        )
        new_order.save()

        # Create OrderItem objects for each item in the cart
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=new_order,
                customer=customer,
                product=cart_item.product,
                restorant=cart_item.restorant,
                amount=cart_item.amouunt,  # Use correct field name here
                quantity=cart_item.quantity,
            )
            new_order.save()
            new_order.order_item.add(order_item)
            new_order.save()

            cart_item.delete()


        # Handle payment method logic
        if payment_method == 'CREDIT/DEBIT/UPI':
            # Logic for credit/debit/UPI payment processing
            pass
        elif payment_method == 'COD':
            # Logic for COD (Cash on Delivery) processing
            pass
        
        # After processing the payment, redirect to the order confirmation page
        return redirect('web:order_confirmation', order_id=new_order.order_id)

    context = {
        'item_total': cart_bill.item_total if cart_bill else 0,
        'offer': cart_bill.offer_applied if cart_bill else 0,
        'delivery': cart_bill.delivery_charges if cart_bill else 0,
        'total': cart_bill.final_amount if cart_bill else 0,
    }

    return render(request, 'web/checkout.html', context=context)







@login_required(login_url='web:login')
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id, customer__user=request.user)
    except Order.DoesNotExist:
        order = None

    context = {
        'order_id': order_id if order else None,
        'order': order,
    }

    return render(request, 'web/order_confirmation.html', context)





@login_required(login_url='web:login')
def account(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    # Retrieve all orders for the customer
    orders = Order.objects.filter(customer=customer).prefetch_related('order_item')[:3]
    bill_details = BillDetails.objects.get(customer=customer)
    selected_address = bill_details.address
    
    # Debugging: Print order IDs
    for order in orders:
        print(f"Order ID: {order.id}")

    # Retrieve all order items for the customer
    order_items = OrderItem.objects.filter(customer=customer)
    
    # Retrieve all restaurants (adjust this if needed)
    restorants = Restorant.objects.all()
    
    context = {
        "restorants": restorants,
        "order_items": order_items,
        "user": user,
        "orders": orders,
        "selected_address":selected_address
    }
    return render(request, 'web/account.html', context=context)


@login_required(login_url='web:login')
def orders(request):
    user = request.user
    customer = Customer.objects.get(user=user)

    # Retrieve all orders for the customer
    orders = Order.objects.filter(customer=customer).prefetch_related('order_item')
    
    # Debugging: Print order IDs
    for order in orders:
        print(f"Order ID: {order.id}")

    # Retrieve all order items for the customer
    order_items = OrderItem.objects.filter(customer=customer)
    
    # Retrieve all restaurants (adjust this if needed)
    restorants = Restorant.objects.all()
    
    context = {
        "restorants": restorants,
        "order_items": order_items,
        "user": user,
        "orders": orders,
    }
    return render(request, 'web/orders.html', context=context)





@login_required(login_url='web:login')
def order_tracking(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)

    # Retrieve the specific order based on the id
    order = Order.objects.get(id=id)

    # Retrieve the order items associated with this specific order
    order_items = OrderItem.objects.filter(customer=customer)

    context = {
        "order": order,
        "order_items": order_items
    }
    
    return render(request, 'web/order_tracking.html', context=context)





def ajaxlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        User =authenticate(request, email=email, password=password)
        if User is not None:
            auth_login(request,User)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            context = {'error_message': 'Invalid email address'}
            return render(request, 'web/ajaxlogin.html', context)
    else:
        return render(request,'web/ajaxlogin.html')







def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_valid': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)





def updatecart(request):
    if request.method == 'POST':
        # Fetching product and cart item
        prod_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Cart.product, id=prod_id)  # Assuming you have a Product model
        
        # Checking if the cart exists for the user
        if Cart.objects.filter(customer__user=request.user, product=product).exists():
            cart_item = Cart.objects.get(customer__user=request.user, product=product)

            # Update the quantity based on increment or decrement
            action = request.POST.get('action')
            if action == 'increment':
                cart_item.quantity += 1
            elif action == 'decrement':
                cart_item.quantity -= 1
                # Ensure the quantity doesn't go below 1
                if cart_item.quantity < 1:
                    cart_item.quantity = 1

            cart_item.save()

            # Return updated cart item data as JSON response
            return JsonResponse({
                "success": True,
                "quantity": cart_item.quantity,
                "total_price": cart_item.quantity * product.price
            })

    return JsonResponse({"success": False, "message": "Invalid request"})







def ajax(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    addresses = Address.objects.filter(customer=customer)
    restorant = None
    cart_amount = 0
    delivery_charges = 50
    discount = 0
    error_message = ""
    success_message = ""
    selected_address = None

    if carts.exists():
        cart_amount = carts.aggregate(Sum('amouunt'))['amouunt__sum']
        restorant = carts.first().restorant
    else:
        cart_amount = 0
        delivery_charges = 50
        discount = 0

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            offer = OfferCupen.objects.get(offer_code=code)
            if offer.is_percentage:
                discount = (float(offer.offer_amount) / 100) * cart_amount
                discount = round(discount)
            else:
                discount = offer.offer_amount
            success_message = "Coupon applied successfully!"
        except OfferCupen.DoesNotExist:
            error_message = "Invalid coupon code. Please try again."

    to_pay_amount = float(cart_amount) + float(delivery_charges) - float(discount)

    if BillDetails.objects.filter(customer=customer).exists():
        bill_details = BillDetails.objects.get(customer=customer)
        bill_details.item_total = cart_amount
        bill_details.final_amount = cart_amount + delivery_charges - float(bill_details.offer_applied)
        bill_details.save()
        selected_address = bill_details.address
    else:
        bill_details = BillDetails.objects.create(
            customer=customer,
            item_total=cart_amount,
            delivery_charges=delivery_charges,
            final_amount=cart_amount + delivery_charges,
            offer_applied=0
        )

    context = {
        "restorant": restorant,
        "carts": carts,
        "cart_amount": cart_amount,
        "delivery_charges": delivery_charges,
        "bill_details": bill_details,
        "to_pay_amount": to_pay_amount,
        "discount": discount,
        "addresses": addresses,
        "error_message": error_message,
        "success_message": success_message,
        "selected_address": selected_address,
    }

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    else:
        return render(request, 'web/ajax.html', context=context)
