from django.db import models
from django.contrib.auth.hashers import make_password


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    opening_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.store_name


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date_joined = models.DateField()
    last_login = models.DateTimeField(blank=True, null=True)  # ← Add this line

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Hash password only if it's not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
     # Define get_email_field_name method to specify the email field for password reset
    @classmethod
    def get_email_field_name(cls):
        return "email"  # This tells Django to use the 'email' field for authentication



class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    menu_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return self.menu_name


class MenuCategory(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = (('menu', 'category'),)

    def __str__(self):
        return f"{self.menu.menu_name} - {self.category.category_name}"


class Offer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    offer_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='special_images/', null=True, blank=True)

    def __str__(self):
        return self.offer_name


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, blank=True)
    price_m = models.DecimalField(max_digits=10, decimal_places=2)
    price_l = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Size for {self.menu.menu_name} (M: {self.price_m}, L: {self.price_l})"
