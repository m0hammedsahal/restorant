from django.contrib import admin

from customer.models import *

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(OfferCupen)
admin.site.register(BillDetails)
admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Order)
