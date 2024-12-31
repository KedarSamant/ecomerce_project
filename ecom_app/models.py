from django.core.exceptions import ValidationError  # Import this for custom validation
from django.core.validators import EmailValidator  # Built-in email validator
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=30)
    price=models.IntegerField(default=0)
    description=models.TextField(max_length=300,default='',null=True,blank=True)
    big_description=models.TextField(max_length=1000,default='',null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image=models.ImageField(upload_to='image')

    class Meta:
        db_table='product'
        ordering=['name']

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table='cart'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Cart)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class UserRegister(UserCreationForm):#this UserCreationForm is inherited from forms.ModelForm
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']


    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

     # Custom validation for the username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isnumeric():
            raise ValidationError("Username cannot be entirely numeric.")
        return username

    # Custom validation for the first name
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name must contain only letters.")
        return first_name

    # Custom validation for the last name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only letters.")
        return last_name

    # Custom validation for the email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_validator = EmailValidator()
        try:
            email_validator(email)  # Validate the email format
        except ValidationError:
            raise ValidationError("Enter a valid email address.")
        return email
    
    # Custom validation for the password
    def clean_password2(self):  # 'password2' is the confirmation password field in UserCreationForm
        password = self.cleaned_data.get('password1')
        if not password:
            raise ValidationError("Password is required.")

        # Ensure the password meets the strength criteria
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

        return password