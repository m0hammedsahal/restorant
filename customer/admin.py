from django.contrib import admin

from customer.models import Customer, Cart, OfferCupen, BillDetails, DeliveryDetails

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(OfferCupen)
admin.site.register(BillDetails)
admin.site.register(DeliveryDetails)
