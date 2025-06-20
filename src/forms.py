# forms.py
from django import forms
from .models import Store, Admin, Category, Menu, MenuCategory, Offer, Size

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['store_name', 'location', 'contact_info', 'opening_date', 'status']
    
    opening_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y')
    )

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['store', 'name', 'email', 'password', 'phone', 'date_joined']
    
    date_joined= forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y')
    )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['admin', 'store', 'menu_name', 'description', 'price', 'image']

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['menu', 'category']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['store', 'offer_name', 'description', 'price', 'image']

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['menu', 'price_m', 'price_l']
