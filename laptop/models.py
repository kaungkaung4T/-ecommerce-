from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image
from datetime import datetime

class Laptop(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2050)
    image = models.ImageField(upload_to="media")
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    #  here ================================================
    # def save(self, *args, **kwargs):
    #     super().save()

        img = Image.open(self.image.path)
        # img = img.resize((300, 300))
        # img.thumbnail((300,300), Image.ANTIALIAS)

        # AWS cant use idk why
        #  here ================================================
        # if img.height > 300 or img.width > 300:
        #     over = (300, 300)
        #     img.thumbnail(over)
        #     img.save(self.image.path, quality=95)


        # else:
        #     img.save(self.image.path, quality=95)

    def discount_percent(self):
        if self.discount:
            self.price = int(self.price)
            self.discount = int(self.discount)
            ez = 100 * (self.price - self.discount) // self.price
            return ez

class item(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    items = models.ForeignKey(Laptop, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=1, null=True, blank=True)
    # title = models.CharField(max_length=50)
    # price = models.FloatField()
    # discount = models.FloatField(null=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    newitem = models.ManyToManyField(item, related_name="item_lists")

    def __str__(self):
        return f"{self.user.username}"

    def total(self):
        new = 0
        for item in self.newitem.all():
            if item.items.discount:
                new += item.items.discount
            else:
                new += item.items.price
        return new

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category")