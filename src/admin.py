from django.contrib import admin
from .models import Store, Admin, Category, Menu, MenuCategory, Offer, Size
from .forms import StoreForm, AdminForm, CategoryForm, MenuForm, MenuCategoryForm, OfferForm, SizeForm

# Common admin class for all models to restrict functionality to only adding
class CommonModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {
            'add': True,     # Only allow adding new items
            'change': False, # Disable editing
            'delete': False, # Disable deleting
        }

# Register each model with its custom form
class StoreAdmin(CommonModelAdmin):
    form = StoreForm
    fields = ['store_name', 'location', 'contact_info', 'opening_date', 'status']

class AdminAdmin(CommonModelAdmin):
    form = AdminForm
    fields = ['store', 'name', 'email', 'password', 'phone', 'date_joined']

class CategoryAdmin(CommonModelAdmin):
    form = CategoryForm
    fields = ['category_name', 'description']

class MenuAdmin(CommonModelAdmin):
    form = MenuForm
    fields = ['admin', 'store', 'menu_name', 'description', 'price', 'image']

class MenuCategoryAdmin(CommonModelAdmin):
    form = MenuCategoryForm
    fields = ['menu', 'category']

class OfferAdmin(CommonModelAdmin):
    form = OfferForm
    fields = ['store', 'offer_name', 'description', 'price', 'image']

class SizeAdmin(CommonModelAdmin):
    form = SizeForm
    fields = ['menu', 'price_m', 'price_l']

# Register models with the admin site using their respective custom admin classes
admin.site.register(Store, StoreAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Size, SizeAdmin)
