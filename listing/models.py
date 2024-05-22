from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.


class User(AbstractUser):  # Ensure this line is present
    email = models.CharField(blank=False,max_length=40)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="User_images/", null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="category_images/",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False)
    description = models.TextField(null=True,blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product_images/")
    
    def __str__(self):
        return self.title
    
    
STATUS = [
    ("Pending","Pending"),
    ("Paid","Paid"),
]
class Transaction(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.CharField(choices=STATUS,max_length=20)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    
    