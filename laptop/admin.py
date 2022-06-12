from django.contrib import admin
from laptop.models import Laptop
from laptop.models import Order
from laptop.models import item
from laptop.models import Category

# Register your models here.
class LaptopAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "description", "image", "price", "discount", "time"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image"]

admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Order)
admin.site.register(item)
admin.site.register(Category, CategoryAdmin)