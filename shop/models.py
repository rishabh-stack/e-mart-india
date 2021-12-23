from django.db import models
from .category import cat, sub_cat


# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=cat())
    subcategory = models.CharField(max_length=300, choices=sub_cat())
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    contact_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=300,default="")
    desc=models.CharField(max_length=3000,default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    phone=models.CharField(max_length=90,default="")
    city=models.CharField(max_length=90)
    state=models.CharField(max_length=90)
    zip_code=models.CharField(max_length=90)
    address=models.CharField(max_length=200)

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.update_desc
