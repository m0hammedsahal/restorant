from django.db import models
from users.models import User
from web.models import Restorant, Fooditem

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'users_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ['-id']
    
    def __str__(self):
        return self.user.email

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    restorant = models.ForeignKey(Restorant, on_delete=models.CASCADE)
    amouunt = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'customer_cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ['-id']
    
    def __str__(self):
        return self.customer.user.email
    


class OfferCupen(models.Model):
    offer_code = models.CharField(max_length=50) 
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_description = models.TextField()

    class Meta:
        db_table = 'customer_offer_cupen'
        verbose_name = 'offer_cupen'
        verbose_name_plural = 'offer_cupens'
        ordering = ['-id']
    
    def __str__(self):
        return self.offer_code

    


class BillDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    offer_applied = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    delivery_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'customer_bill_detail'
        verbose_name = 'bill_detail'
        verbose_name_plural = 'bill_details'
        ordering = ['-id']
    
    def __str__(self):
        return self.customer.user.email




class DeliveryDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    special_instructions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'customer_delivery_detail'
        verbose_name = 'delivery_detail'
        verbose_name_plural = 'delivery_details'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.customer.user.email} - {self.address_line1}, {self.city}'
