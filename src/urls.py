from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),    path('about/', views.aboutpage, name='about'),
    path('menu/', views.menupage, name='menu'),  path('order/', views.orderpage, name='order'),
     path('login/', views.loginpage, name='login'),  path('srcadmin/', views.adminpage, name='srcadmin'),
     path('home/', views.homepage, name='homepage'), path('logout/', views.logout_view, name='logout'),
     path('srcadmin/update/store/<int:id>/', views.update_store, name='update_store'),
      path('srcadmin/update/admin/<int:id>/', views.update_admin, name='update_admin'),
      path('srcadmin/stores/', views.get_all_stores, name='get_all_stores'),
       path('srcadmin/update/category/<int:id>/', views.update_category, name='update_category'),
       path('srcadmin/admins/', views.get_all_admins, name='get_all_admins'),
       path('srcadmin/update/menu/<int:id>/', views.update_menu, name='update_menu'),
       path('srcadmin/menus/', views.get_all_menus, name='get_all_menus'),
       path('srcadmin/categories/', views.get_all_categories, name='get_all_categories'),
       path('srcadmin/update/menucategory/<int:id>/', views.update_menucategory, name='update_menucategory'),
       path('srcadmin/update/offer/<int:id>/', views.update_offer, name='update_offer'),
       path('srcadmin/update/size/<int:id>/', views.update_size, name='update_size'),
       path('srcadmin/delete/<str:model_name>/<int:pk>/', views.delete_item, name='delete_item'),
     path('add/store/', views.add_store, name='add_store'),
    path('add/admin/', views.add_admin, name='add_admin'),
    path('add/category/', views.add_category, name='add_category'),
    path('add/menu/', views.add_menu, name='add_menu'),
    path('add/menu-category/', views.add_menu_category, name='add_menu_category'),
    path('add/offer/', views.add_offer, name='add_offer'),
    path('add/size/', views.add_size, name='add_size'),
     path('form/<str:model_name>/', views.dynamic_form, name='dynamic_form'),
    path('submit/<str:model_name>/', views.submit_form, name='submit_form'),
      path('send_admin_reset_link/', views.send_admin_reset_link, name='send_admin_reset_link'),
      path('admin-password-reset-confirm/<uidb64>/<token>/', views.admin_password_reset_confirm, name='admin_password_reset_confirm'),




]

