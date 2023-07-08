from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Wood(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_woods' )
    name = models.CharField(max_length=30)
    telephone = models.IntegerField()
    latitude = models.DecimalField(decimal_places=16, max_digits=20)
    longitude = models.DecimalField(decimal_places=16, max_digits=20)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='wood')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.name + " by " + self.owner.username

class Machinery(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_machinery' )
    name = models.CharField(max_length=30)
    telephone = models.IntegerField()
    latitude = models.DecimalField(decimal_places=16, max_digits=20)
    longitude = models.DecimalField(decimal_places=16, max_digits=20)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='machinery')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        
        verbose_name_plural = "Machineries"

    def __str__(self) -> str:
        return self.name + " by " +self.owner.username
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product')
    average_rating = models.DecimalField(max_digits=2,decimal_places=1,default=0)
    discount = models.DecimalField(max_digits=2, decimal_places=2,default=0)
    brand=models.CharField(max_length=50, default="Unknown")
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']

class ProductRating(models.Model):
    user = models.ForeignKey(User, related_name='rated_products',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='ratings',on_delete=models.CASCADE)
    rate = models.IntegerField()
    description = models.CharField(max_length=200)

    def __str__(self) -> str:
        return  self.product.name + " review by " + self.user.username
    
    class Meta:
        ordering = ['rate']
    