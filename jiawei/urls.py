from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/save_location/', views.save_location, name='save_location'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('taboo_manage/', views.taboo_manage, name='taboo_manage'),
    
    path('dishes/', views.dish_list, name='dish_list'),
    path('dishes/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('dishes/add/', views.dish_add, name='dish_add'),
    path('dishes/<int:pk>/edit/', views.dish_edit, name='dish_edit'),
    path('dishes/<int:pk>/delete/', views.dish_delete, name='dish_delete'),
    
    path('fruits/', views.fruit_list, name='fruit_list'),
    path('fruits/<int:pk>/', views.fruit_detail, name='fruit_detail'),
    path('fruits/add/', views.fruit_add, name='fruit_add'),
    path('fruits/<int:pk>/edit/', views.fruit_edit, name='fruit_edit'),
    path('fruits/<int:pk>/delete/', views.fruit_delete, name='fruit_delete'),
    
    path('drinks/', views.drink_list, name='drink_list'),
    path('drinks/<int:pk>/', views.drink_detail, name='drink_detail'),
    path('drinks/add/', views.drink_add, name='drink_add'),
    path('drinks/<int:pk>/edit/', views.drink_edit, name='drink_edit'),
    path('drinks/<int:pk>/delete/', views.drink_delete, name='drink_delete'),
    
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('summary/', views.summary, name='summary'),
    path('generate_purchase_text/', views.generate_purchase_text, name='generate_purchase_text'),
    path('calculate_cost/', views.calculate_cost, name='calculate_cost'),
    path('submit_order/', views.submit_order, name='submit_order'),
    
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/finish/', views.mark_order_finish, name='mark_order_finish'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    path('orders/', views.order_list, name='order_list'),
    path('cart/count/', views.cart_count, name='cart_count'),
    
    path('markets/', views.market_list, name='market_list'),
    path('markets/add/', views.market_add, name='market_add'),
    path('markets/<int:pk>/edit/', views.market_edit, name='market_edit'),
    path('markets/<int:pk>/delete/', views.market_delete, name='market_delete'),
    path('markets/nearby/', views.market_nearby, name='market_nearby'),
    
    path('prices/', views.price_list, name='price_list'),
    path('prices/location/', views.price_by_location, name='price_by_location'),
    path('prices/add/', views.price_add, name='price_add'),
    
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/add/', views.stock_add, name='stock_add'),
    path('stocks/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stocks/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    
    path('materials/', views.material_list, name='material_list'),
    path('materials/add/', views.material_add, name='material_add'),
    path('materials/<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('materials/<int:pk>/delete/', views.material_delete, name='material_delete'),
    
    path('ai_recommend/', views.ai_recommend, name='ai_recommend'),
    path('add_recommend_to_cart/', views.add_recommend_to_cart, name='add_recommend_to_cart'),
    
    path('statistics/', views.statistics, name='statistics'),
    
    path('collect/', views.collect, name='collect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)