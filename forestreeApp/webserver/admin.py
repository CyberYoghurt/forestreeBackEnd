from django.contrib import admin
from .models import Wood,Machinery,Product,ProductRating

# Register your models here.
admin.site.register(Wood)
admin.site.register(Machinery)
admin.site.register(Product)
admin.site.register(ProductRating)

