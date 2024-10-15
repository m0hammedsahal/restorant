from django import forms
from web.models import *
from customer.models import *




class RestorantCategoryForm(forms.ModelForm):
    class Meta:
        model = RestorantCategory  # Correct 'models' to 'model'
        fields = ['name', 'image']  # Ensure this is a list or tuple

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }



class RestorantForm(forms.ModelForm):
    class Meta:
        model = Restorant
        fields = ['name', 'discription', 'rating', 'time', 'discount', 'image', 'category']

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Restorant Name"}),
            "discription": forms.TextInput(attrs={"class": "form-control", "placeholder": "Description"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Rating"}),
            "time": forms.TextInput(attrs={"class": "form-control", "placeholder": "Time"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Discount"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }




class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['image', 'restorant']
        
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "restorant": forms.Select(attrs={"class": "form-control"}),
        }


class FoodcategoryForm(forms.ModelForm):
    class Meta:
        model = Foodcategory
        fields = ['name', 'restorant']
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}),
            "restorant": forms.Select(attrs={"class": "form-control"}),
        }




class FooditemForm(forms.ModelForm):
    class Meta:
        model = Fooditem
        fields = ['name', 'title', 'image', 'price', 'is_veg', 'foodcategory']
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Food item name"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
            "is_veg": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "foodcategory": forms.Select(attrs={"class": "form-control"}),
        }

   
class FooditemfcForm(forms.ModelForm):
    class Meta:
        model = Fooditem
        fields = ['name', 'title', 'image', 'price', 'is_veg', 'foodcategory']
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Food item name"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
            "is_veg": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

   


class OfferCupenForm(forms.ModelForm):
    class Meta:
        model = OfferCupen
        fields = ['offer_code', 'title', 'offer_amount', 'offer_description', 'is_percentage', 'start_time', 'end_time']
        
        widgets = {
            "offer_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Offer Code"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "offer_amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Offer Amount"}),
            "offer_description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Offer Description", "rows": 3}),
            "is_percentage": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "start_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }


class ManagerLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )