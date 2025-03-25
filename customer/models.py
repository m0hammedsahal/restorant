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
    offer_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    offer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_description = models.TextField()
    is_percentage = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

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
    address = models.ForeignKey('customer.Address', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'customer_bill_detail'
        verbose_name = 'bill_detail'
        verbose_name_plural = 'bill_details'
        ordering = ['-id']
    
    def __str__(self):
        return self.customer.user.email



    

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    pin_code = models.CharField(max_length=6)
    mobile_no = models.CharField(max_length=13, default="+91")
    address_type = models.CharField(max_length=50, choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')], default='home')

    class Meta:
        db_table = 'customer_address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.address}, {self.pin_code}"



class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    restorant = models.ForeignKey(Restorant, on_delete=models.CASCADE)
    amount = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'customer_OrderItem'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.customer.user.email} - {self.product.name}'






class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CREDIT/DEBIT/UPI', 'Credit/Debit/UPI'),
        ('COD', 'Cash on Delivery'),
        # Add more payment methods as needed
    ]
    STATUS_CHOICES = [
        ('Preparing', 'Preparing'),
        ('Ready for Pickup/Delivery', 'Ready for Pickup/Delivery'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    order_id = models.CharField(max_length=255, unique=True)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    offer = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    order_item = models.ManyToManyField(OrderItem)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')  # New field added
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Preparing')
    
    class Meta:
        db_table = 'customer_Order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']
    
    def __str__(self):
        return f'Order {self.order_id} for {self.customer.user.email}'



