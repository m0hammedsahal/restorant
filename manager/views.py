from main.decorators import allow_manager

from main.functions import generate_form_errors


# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from users.models import User
from customer.models import *


from web.models import *


from django.contrib.auth import logout as auth_logout

from django.contrib import messages
from .forms import *
 # Ensure only logged-in users can access the index view


@login_required(login_url='manager:login')
@allow_manager
def index(request):
    
    return render(request, 'manager/index.html')

def unauthorized_access(request):
    
    return render(request, 'manager/unauthorized_access.html')


def login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_manager:  # Check if the user has manager rights
                    auth_login(request, user)  # Use Django's login function with alias
                    return redirect('manager:index')
                else:
                    messages.error(request, 'Unauthorized access.')
                    return HttpResponse("Unauthorized", status=401)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid form data.') 
    else:
        form = ManagerLoginForm()

    return render(request, 'manager/login.html', {"form": form})




def logout_view(request):
    auth_logout(request)
    return redirect('manager:login')  # Redirect to the login page


def register(request):
    
    return render(request, 'manager/register.html')

# store_category_list

def store_category_list(request):
    instances = RestorantCategory.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/store_category_list.html', context=context)






def store_category_add(request):
    if request.method == 'POST':
        form = RestorantCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:store_category_list'))
    else:
        form = RestorantCategoryForm()

    return render(request, 'manager/forms/store_category_add_form.html', {'form': form})





def store_category_edit(request, id):
    store_category = get_object_or_404(RestorantCategory, id=id)

    if request.method == 'POST':
        form = RestorantCategoryForm(request.POST, request.FILES, instance=store_category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:store_category_list'))
    else:
        form = RestorantCategoryForm(instance=store_category)

    return render(request, 'manager/forms/store_category_add_form.html', {'form': form, 'is_edit': True, 'store_category': store_category})



def store_category_delete(request, id):
    instance = RestorantCategory.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# slide_list

def slide_list(request):
    instances = Slide.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/slide_list.html', context=context)


def slide_add(request):
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:slide_list'))
    else:
        form = SlideForm()

    return render(request, 'manager/forms/slide_add_form.html', {'form': form})


def slide_edit(request, id):
    slide = get_object_or_404(Slide, id=id)

    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:slide_list'))
    else:
        form = SlideForm(instance=slide)

    return render(request, 'manager/forms/slide_add_form.html', {'form': form, 'is_edit': True, 'slide': slide})



def slide_delete(request, id):
    instance = Slide.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# restorant_list

def restorant_list(request):
    instances = Restorant.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/restorant_list.html', context=context)



def restorant_add(request):
    if request.method == 'POST':
        form = RestorantForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:restorant_list'))
        else:
            message = generate_form_errors(form)
            form = RestorantForm()
            context ={
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, 'manager/forms/restorant_add_form.html', context=context)
    else:
        form = RestorantForm()
        context = {
            "name": "Add Restorant",
            "form": form,
        }
        return render(request, 'manager/forms/restorant_add_form.html', context=context)



def restorant_edit(request, id):
    store = get_object_or_404(Restorant, id=id)

    if request.method == 'POST':
        form = RestorantForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:restorant_list'))
    else:
        form = RestorantForm(instance=store)

    return render(request, 'manager/forms/restorant_add_form.html', {'form': form, 'is_edit': True, 'store': store})




def restorant_delete(request, id):
    instance = Restorant.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# food_category_list

def food_category_list(request):
    instances = Foodcategory.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/food_category_list.html', context=context)


def food_category_add(request):
    if request.method == 'POST':
        form = FoodcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:food_category_list'))
    else:
        form = FoodcategoryForm()

    return render(request, 'manager/forms/food_category_add_form.html', {'form': form})


def food_category_edit(request, id):
    foodcategory = get_object_or_404(Foodcategory, id=id)

    if request.method == 'POST':
        form = FoodcategoryForm(request.POST, instance=foodcategory)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:food_category_list'))
    else:
        form = FoodcategoryForm(instance=foodcategory)

    return render(request, 'manager/forms/food_category_add_form.html', {'form': form, 'is_edit': True, 'foodcategory': foodcategory})

def food_category_delete(request, id):
    instance = Foodcategory.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# food_item_list

def food_item_list(request):
    instances = Fooditem.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/food_item_list.html', context=context)





def food_item_add(request, id):
    restorant = Restorant.objects.get(id=id)
    restorantname = restorant.name
    restorantimage = restorant.image
    foodcategories = Foodcategory.objects.filter(restorant=restorant)
    if request.method == 'POST':
        form = FooditemForm(request.POST, request.FILES)
        foodcategory = request.POST.get('foodcategory')
        foodcategory = Foodcategory.objects.get(id=foodcategory)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.restorant = restorant
            instance.foodcategory = foodcategory
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:food_item_list'))
        else:
            message = generate_form_errors(form)
            form = FooditemForm()
            context ={
                "error": True,
                "message": message,
                "form": form,
                "foodcategories": foodcategories,
                "restorantname": restorantname,
                "restorantimage": restorantimage
            }
            return render(request, 'manager/forms/food_item_add_form.html', context=context)
    else:
        form = FooditemForm()
        context = {
            "name": "Add Food ",
            "form": form,
            "foodcategories": foodcategories,
            "restorantname": restorantname,
            "restorantimage": restorantimage
        }
        return render(request, 'manager/forms/food_item_add_form.html', context=context)





# def food_item_add_f_cate(request, id):
#     foodcategory = Foodcategory.objects.get(id=id)
#     restorantname = foodcategory.restorant
#     foodcategoryname = Foodcategory.objects.filter(restorant=restorantname)
#     print(restorantname)
#     if request.method == 'POST':
#         form = FooditemfcForm(request.POST, request.FILES)
#         foodcategory = request.POST.get('foodcategory')
#         foodcategory = Foodcategory.objects.get(id=foodcategory)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.restorant = foodcategory
#             instance.foodcategory = foodcategory
#             instance.save()
            
#             return HttpResponseRedirect(reverse('manager:food_item_list'))
#         else:
#             message = generate_form_errors(form)
#             form = FooditemfcForm()
#             context ={
#                 "error": True,
#                 "message": message,
#                 "form": form,
#                 "foodcategoryname": foodcategoryname,
#                 "restorantname": restorantname
#             }
#             return render(request, 'manager/forms/food_item_f_cate.html', context=context)
#     else:
#         form = FooditemfcForm()
#         context = {
#             "name": "Add Food ",
#             "form": form,
#             "foodcategoryname": foodcategoryname,
#             "restorantname": restorantname
#         }
#         return render(request, 'manager/forms/food_item_f_cate.html', context=context)


def food_item_add_f_cate(request, id):
    # Get the food category by its ID
    foodcategory = Foodcategory.objects.get(id=id)
    # Get the associated restaurant from the food category
    restorant = foodcategory.restorant
    foodcategoryname = foodcategory.name
    # Filter food categories associated with this restaurant (if needed)
    
    if request.method == 'POST':
        form = FooditemfcForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # Set the restaurant and food category
            instance.restorant = restorant
            instance.foodcategory = foodcategory
            instance.save()
            
            return HttpResponseRedirect(reverse('manager:food_item_list'))
        else:
            message = generate_form_errors(form)
            context = {
                "error": True,
                "message": message,
                "form": form,
                "foodcategoryname": foodcategoryname,
                "restorantname": restorant  # Pass the restaurant name to the context
            }
            return render(request, 'manager/forms/food_item_f_cate.html', context=context)
    else:
        form = FooditemfcForm()
        context = {
            "name": "Add Food Item",
            "form": form,
            "foodcategoryname": foodcategoryname,
            "restorantname": restorant  # Pass the restaurant name to the context
        }
        return render(request, 'manager/forms/food_item_f_cate.html', context=context)





def food_item_edit(request, id):
    fooditem = get_object_or_404(Fooditem, id=id)

    if request.method == 'POST':
        form = FooditemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:food_item_list'))
    else:
        form = FooditemForm(instance=fooditem)

    return render(request, 'manager/forms/food_item_add_form.html', {'form': form, 'is_edit': True, 'fooditem': fooditem})



def food_item_delete(request, id):
    instance = Fooditem.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






# offers_list

def offers_list(request):
    instances = OfferCupen.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/offers_list.html', context=context)


def offers_add(request):
    if request.method == 'POST':
        form = OfferCupenForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:offers_list'))
    else:
        form = OfferCupenForm()

    return render(request, 'manager/forms/offers_add_form.html', {'form': form})

def offers_edit(request, id):
    offercupen = get_object_or_404(OfferCupen, id=id)

    if request.method == 'POST':
        form = OfferCupenForm(request.POST, instance=offercupen)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manager:offers_list'))
    else:
        form = OfferCupenForm(instance=offercupen)

    return render(request, 'manager/forms/offers_add_form.html', {'form': form, 'is_edit': True, 'offercupen': offercupen})


def offers_delete(request, id):
    offercupen = get_object_or_404(OfferCupen, id=id)
    offercupen.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def orders_track_list(request):
    instances = Order.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/orders_track_list.html', context=context)



def order_track(request, id):
    instance = Order.objects.get(id=id)
    if instance.order_status == 'Preparing':
        instance.order_status = 'Ready for Pickup/Delivery'
        instance.save()

    elif instance.order_status == 'Ready for Pickup/Delivery':
        instance.order_status = 'Dispatched'
        instance.save()

    elif instance.order_status == 'Dispatched':
        instance.order_status = 'Delivered'
        instance.save()
    
    
    # return render(request, 'manager/forms/order_track.html', context=context)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cancel_order(request, id):
    instance = Order.objects.get(id=id)
    instance.order_status = 'Cancelled'
    instance.save()



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# orders_list

def orders_list(request):
    instances = Order.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/orders_list.html', context=context)



def orders_edit(request):
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def orders_delete(request, id):
    instance = Order.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# users

def users_list(request):
    instances = User.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/users_list.html', context=context)


def users_delete(request, id):
    instance = User.objects.get(id=id)
    instance.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))