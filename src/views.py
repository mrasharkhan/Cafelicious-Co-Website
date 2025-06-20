from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Admin, Store, Category, Menu, MenuCategory, Offer, Size
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.apps import apps
from .forms import StoreForm, AdminForm, CategoryForm, MenuForm, MenuCategoryForm, OfferForm, SizeForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import json

#homepage
def homepage(request):
    special_offer = Offer.objects.all()

    return render(request, 'home.html', {
        'MEDIA_URL': settings.MEDIA_URL,
        'special_offer': special_offer,
    })  
 
#aboutpage
def aboutpage(request):
    return render(request, 'about.html', {
        'MEDIA_URL': settings.MEDIA_URL
    })
#menupage
def menupage(request):
    # Fetch all categories
    categories = Category.objects.all()
    
    # Fetch all menu items
    menu_items = Menu.objects.all().select_related('store', 'admin')
    
    # Fetch menu categories to map menu items to their categories
    menu_categories = MenuCategory.objects.all().select_related('menu', 'category')
    
    # Fetch sizes for menu items
    sizes = Size.objects.all().select_related('menu')
    
    # Fetch today's special offer (example: latest offer or one with valid date)
    special_offer = Offer.objects.all()

    # Organize menu items by category for easier template rendering
    category_menu_map = {}
    for category in categories:
        category_menu_map[category.category_name] = []
        for menu_item in menu_items:
            # Check if this menu item belongs to the current category
            if menu_categories.filter(menu=menu_item, category=category).exists():
                # Get sizes for this menu item
                item_sizes = sizes.filter(menu=menu_item)
                category_menu_map[category.category_name].append({
                    'menu_item': menu_item,
                    'sizes': item_sizes
                })

    return render(request, 'menu.html', {
        'MEDIA_URL': settings.MEDIA_URL,
        'category_menu_map': category_menu_map,
        'special_offer': special_offer,
    })

#orderpage
def orderpage(request):
    return render(request, 'order.html' , {
        'MEDIA_URL': settings.MEDIA_URL
    })

#login


def loginpage(request):
    if request.method == 'POST':
        # Get the form data
        email = request.POST.get('email')  # Use `get` to avoid KeyError
        password = request.POST.get('password')

        try:
            # Check if the admin with the given email exists
            admin = Admin.objects.get(email=email)

            # Check if the provided password matches the stored hashed password
            if check_password(password, admin.password):
                # If credentials match, log the admin in
                request.session['admin_id'] = admin.admin_id  # Store admin ID in session

                # Redirect to the admin dashboard after login
                return redirect('srcadmin')  # Replace with the actual redirect URL name
            else:
                messages.error(request, "Incorrect password. Please try again.")
        except Admin.DoesNotExist:
            messages.error(request, "Admin with this email does not exist. Please try again.")

    return render(request, 'login.html', {
        'MEDIA_URL': settings.MEDIA_URL
    })


#admin
def adminpage(request):

    # Check if the user is logged in by checking the session
    if 'admin_id' not in request.session:
        return redirect('login')  # Redirect to the login page if not logged in
    try:
        admin = Admin.objects.get(pk=request.session['admin_id'])  # Fetch admin from DB
    except Admin.DoesNotExist:
        return redirect('login')  # Handle if ID is invalid
    # If logged in, render the admin page
    stores = Store.objects.all()
    all_admins = Admin.objects.select_related('store').all()
   

    categories = Category.objects.all()
    all_menu=Menu.objects.select_related('store','admin').all()
    menucategories=MenuCategory.objects.select_related('menu','category').all()
    offers=Offer.objects.select_related('store').all()
    sizes=Size.objects.select_related('menu').all()
    return render(request, 'Admin.html', {
        'MEDIA_URL': settings.MEDIA_URL, 'admin': admin, 'stores': stores, 'all_admins': all_admins, 'categories':categories,
    'all_menu':all_menu, 'menucategories': menucategories, 'offers':offers, 'sizes':sizes})

#logout
def logout_view(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "You have successfully logged out.")
    return redirect('login') # Redirect to login page

def update_store(request, id):
    store = get_object_or_404(Store, pk=id)

    if request.method == 'POST':
        store.store_name = request.POST.get('name')
        store.location = request.POST.get('location')
        store.contact_info = request.POST.get('contact')
        store.opening_date = request.POST.get('date_opened')  # make sure the name matches your form
        store.status = request.POST.get('status')
        store.save()
        return redirect('/srcadmin')  # or wherever your admin table is

    # For GET (when you click "edit" button and fetch via JS)
    return JsonResponse({
        'store_id': store.store_id,
        'store_name': store.store_name,
        'location': store.location,
        'contact_info': store.contact_info,
        'opening_date': store.opening_date.strftime('%Y-%m-%d'),  # formatted for <input type="date">
        'status': store.status
    })


def update_admin(request, id):
    admin = get_object_or_404(Admin, pk=id)

    if request.method == 'POST':
        admin.name = request.POST.get('name')

        # Get store ID from the hidden input
        store_id = request.POST.get('store')  # This is from the hidden input
        if store_id:
            try:
                # Fetch the Store object using the store ID
                admin.store = Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                admin.store = None  # In case the store doesn't exist

        admin.email = request.POST.get('email')

        # Only update password if a new one is provided
        password_input = request.POST.get('password')
        if password_input:  # Check if the password field is not empty
            admin.password = password_input  # Will be auto-hashed in model's save()

        admin.phone = request.POST.get('phone')
        admin.date_joined = request.POST.get('date_joined')
        admin.save()  # Save the admin object (with the password being auto-hashed)

        return redirect('/srcadmin')  # Redirect to the admin list page after update

    # For GET request, return the admin data with store name and ID for the frontend
    return JsonResponse({
        'admin_id': admin.pk,
        'name': admin.name,
        'store': admin.store.store_name if admin.store else '',  # Store name
        'store_id': admin.store.pk if admin.store else '',  # Store ID for form
        'email': admin.email,
        'password': '',  # Don't return hashed password for security
        'phone': admin.phone,
        'date_joined': admin.date_joined.strftime('%Y-%m-%d'),
    })


def update_offer(request, id):
    offer = get_object_or_404(Offer, pk=id)

    if request.method == 'POST':
        offer.offer_name = request.POST.get('offer_name')

        # Get store ID from the hidden input
        store_id = request.POST.get('store')  # This is from the hidden input
        if store_id:
            try:
                # Fetch the Store object using the store ID
                offer.store = Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                offer.store = None  # In case the store doesn't exist

        offer.description = request.POST.get('offer_description')
        offer.price = request.POST.get('offer_price')
        if 'offer_image' in request.FILES:
            offer.image = request.FILES['offer_image']
        else:
            # Keep the previous image if no new one is uploaded
            offer.image = offer.image

        offer.save()

        return redirect('/srcadmin')  # Redirect to the admin list page after update

    # For GET request, return the admin data with store name and ID for the frontend
    return JsonResponse({
        'offer_id': offer.offer_id,
        'offer_name': offer.offer_name,
        'store': offer.store.store_name if offer.store else '',  # Store name
        'store_id': offer.store.pk if offer.store else '',  # Store ID for form
        'offer_description': offer.description,
        'offer_price': offer.price,
        'offer_image': offer.image.url if offer.image else '',  # Image URL, empty string if no image
    })

def update_category(request, id):
    # Retrieve the category object to be updated
    category = get_object_or_404(Category, pk=id)

    if request.method == 'POST':
        # Update the category fields from the form data
        category.category_name = request.POST.get('category_name')
        category.description = request.POST.get('description')
        category.save()  # Save the updated category object
        
        # Redirect after successful update (you can adjust this URL)
        return redirect('/srcadmin')  # or wherever your admin category table is

    # For GET request (fetch data for modal)
    return JsonResponse({
        'category_id': category.category_id,
        'category_name': category.category_name,
        'description': category.description
    })


def update_menu(request, id):
    menu = get_object_or_404(Menu, pk=id)

    if request.method == 'POST':
        menu.menu_name = request.POST.get('name')

        # Get store ID and admin ID from the hidden input
        store_id = request.POST.get('store')  # This is from the hidden input
        admin_id = request.POST.get('admin')
        
        if store_id:
            try:
                # Fetch the Store object using the store ID
                menu.store = Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                menu.store = None  # In case the store doesn't exist
        
        if admin_id:
            try:
                # Fetch the Admin object using the admin ID
                menu.admin = Admin.objects.get(pk=admin_id)
            except Admin.DoesNotExist:
                menu.admin = None  # In case the admin doesn't exist

        menu.description = request.POST.get('description')
        menu.price = request.POST.get('price')

        # Update image if new one is uploaded
        if 'image' in request.FILES:
            menu.image = request.FILES['image']
        else:
            # Keep the previous image if no new one is uploaded
            menu.image = menu.image

        menu.save()

        return redirect('/srcadmin')  # Redirect to the admin list page after update

    # For GET request, return the menu data with store and admin information
    return JsonResponse({
        'admin_id': menu.admin.pk if menu.admin else '',  # Admin ID for form
        'admin': menu.admin.email if menu.admin else '',  # Admin name for form
        'store': menu.store.store_name if menu.store else '',  # Store name
        'store_id': menu.store.pk if menu.store else '',  # Store ID for form
        'menu_id': menu.menu_id,
        'menu_name': menu.menu_name,
        'description': menu.description,
        'price': menu.price,
        'image': menu.image.url if menu.image else '',  # Image URL, empty string if no image
    })

def update_menucategory(request, id):
    menucategory = get_object_or_404(MenuCategory, pk=id)

    if request.method == 'POST':

        # Get store ID and admin ID from the hidden input
        category_id = request.POST.get('category')  # This is from the hidden input
        menu_id = request.POST.get('menu')
        
        if category_id:
            try:
                # Fetch the Store object using the store ID
                menucategory.category = Category.objects.get(pk=category_id)
            except Category.DoesNotExist:
                menucategory.category = None  # In case the store doesn't exist
        
        if menu_id:
            try:
                # Fetch the Admin object using the admin ID
                menucategory.menu = Menu.objects.get(pk=menu_id)
            except Menu.DoesNotExist:
                menucategory.menu = None  # In case the admin doesn't exist

       
        menucategory.save()

        return redirect('/srcadmin')  # Redirect to the admin list page after update

    # For GET request, return the menu data with store and admin information
    return JsonResponse({
        'category_id': menucategory.category.pk if menucategory.category else '',  # category ID for form
        'category': menucategory.category.category_name if menucategory.category else '',  # category name for form
        'menu': menucategory.menu.menu_name if menucategory.menu else '',  # category name
        'menu_id': menucategory.menu.menu_id if menucategory.menu else '',  # category ID for form
        'menucategory_id': menucategory.pk,
    })

def update_size(request, id):
    size = get_object_or_404(Size, pk=id)

    if request.method == 'POST':

       
        menu_id = request.POST.get('menu')
    
        
        if menu_id:
            try:
                
                size.menu = Menu.objects.get(pk=menu_id)
            except Menu.DoesNotExist:
                size.menu = None  

       
        size.save()

        return redirect('/srcadmin')  

    return JsonResponse({
        'id': size.id , 
        'menu': size.menu.menu_name if size.menu else '',  
        'menu_id': size.menu.menu_id if size.menu else '',  
        'price_m': size.price_m,
        'price_l': size.price_l,
    })



# for dropdown name, email links with ids for frontend
#this helps to populated data without remembering foreign key ids

def get_all_stores(request):
    stores = Store.objects.all().values('store_id', 'store_name')
    return JsonResponse([
        {'id': store['store_id'], 'name': store['store_name']}
        for store in stores
    ], safe=False)

def get_all_admins(request):
    admins = Admin.objects.all().values('admin_id', 'email')
    return JsonResponse([
        {'id': admin['admin_id'], 'email': admin['email']}
        for admin in admins
    ], safe=False)

def get_all_menus(request):
    menus = Menu.objects.all().values('menu_id', 'menu_name')
    return JsonResponse([
        {'id': menu['menu_id'], 'name': menu['menu_name']}
        for menu in menus
    ], safe=False)

def get_all_categories(request):
    categories = Category.objects.all().values('category_id', 'category_name')
    return JsonResponse([
        {'id': category['category_id'], 'name': category['category_name']}
        for category in categories
    ], safe=False)

@require_http_methods(["DELETE"])
def delete_item(request, model_name, pk):
    try:
        # Dynamically get model class
        Model = apps.get_model('src', model_name.capitalize())

        # Get object or 404
        obj = get_object_or_404(Model, pk=pk)
        obj.delete()

        return JsonResponse({'success': True})
    except LookupError:
        return JsonResponse({'success': False, 'error': f"Model '{model_name}' not found."})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def redirect_to_add(request, model_name):
    return redirect(f'/admin/{model_name}/add/')



def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:src_store_changelist')  # Redirect to admin page after success
    else:
        form = StoreForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:src_admin_changelist')  # Redirect to admin page after success
    else:
        form = AdminForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:src_category_changelist')  # Redirect to admin page after success
    else:
        form = CategoryForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin:src_menu_changelist')  # Redirect to admin page after success
    else:
        form = MenuForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_menu_category(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:src_menucategory_changelist')  # Redirect to admin page after success
    else:
        form = MenuCategoryForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin:src_offer_changelist')  # Redirect to admin page after success
    else:
        form = OfferForm()
    return render(request, 'admin/add_form.html', {'form': form})

def add_size(request):
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:src_size_changelist')  # Redirect to admin page after success
    else:
        form = SizeForm()
    return render(request, 'admin/add_form.html', {'form': form})

model_forms = {
    'store': StoreForm,
    'admin': AdminForm,
    'category': CategoryForm,
    'menu': MenuForm,
    'menu-category': MenuCategoryForm,
    'offer': OfferForm,
    'size': SizeForm,
}

def dynamic_form(request, model_name):
    form_class = model_forms.get(model_name.lower())
    if not form_class:
        return JsonResponse({'error': 'Invalid model'}, status=400)
    form = form_class()
    return render(request, 'admin/partials/form_content.html', {'form': form, 'model_name': model_name})

def submit_form(request, model_name):
    form_class = model_forms.get(model_name.lower())
    if not form_class:
        return JsonResponse({'error': 'Invalid model'}, status=400)
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return render(request, 'admin/partials/form_content.html', {'form': form, 'model_name': model_name})



def send_admin_reset_link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            admin_user = Admin.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(admin_user.pk))
            token = default_token_generator.make_token(admin_user)

            reset_link = request.build_absolute_uri(f"/admin-password-reset-confirm/{uid}/{token}/")

            subject = "Reset Your Admin Password"
            message = render_to_string("emails/admin_password_reset_email.txt", {
                "reset_link": reset_link,
                "email": email,
            })
            send_mail(subject, message, "khanashar901@gmail.com", [email])

            return JsonResponse({"success": True, "message": "Password reset link sent."})

        except Admin.DoesNotExist:
            return JsonResponse({"success": False, "message": "Admin with this email does not exist."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request."})

def admin_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        admin_user = Admin.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Admin.DoesNotExist):
        admin_user = None

    if admin_user is not None and default_token_generator.check_token(admin_user, token):
        if request.method == 'POST':
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            if new_password and new_password == confirm_password:
                admin_user.password = make_password(new_password)  # Use this to hash password
                admin_user.save()
                return render(request, "emails/reset_complete.html")
            else:
                return render(request, "emails/admin_reset_form.html", {
                    "validlink": True,
                    "error": "Passwords do not match."
                })
        return render(request, "emails/admin_reset_form.html", {"validlink": True})
    else:
        return render(request, "emails/admin_reset_form.html", {"validlink": False})