from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path("", views.home, name="home"),
    path('search/', views.search_products, name='search'),
    path('load-more-products/', views.load_more_products, name='load_more_products'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),

    
    
    
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password_page, name='forgot_password'),
    path('reset-password/', views.reset_password_page, name='reset_password'),

    
    
    
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    
    path("category/<slug:slug>/", views.category_products, name="category_products"),
    path('electronics/', views.electronics_catalog, name='electronics_catalog'),
    path('furniture/', views.furniture_catalog, name='furniture_catalog'),
    path("tv-appliances/", views.tv_appliances_catalog, name="tv_appliances"),
    path('grocery/', views.grocery_catalog, name='grocery_catalog'),

    
    path("fashion/", views.fashion, name="fashion_catalog"),
    path('fashion-item/<int:product_id>/', views.fashion_detail, name='fashion_detail'),

    
    
    
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-fashion-cart/<int:item_id>/', views.add_fashion_to_cart, name='add_fashion_to_cart'),
    path('add-to-cart-ajax/', add_to_cart_ajax, name='add_to_cart_ajax'),
    
    
    path('plus-cart/<int:cart_id>/', views.plus_cart, name='plus_cart'),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name='minus_cart'),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name='remove_cart'),

    
    
    
    
    path('checkout/cart/', views.cart_checkout_summary, name='cart_checkout_summary'),

    
    path('checkout/product/<int:product_id>/', views.checkout_summary, name='checkout_summary'),
    
    
    path('checkout/fashion/<int:product_id>/', views.fashion_checkout_summary, name='fashion_checkout_summary'),

    
    
    
    
    path('payment/<str:item_type>/<int:item_id>/', views.payment_page, name='payment_page'),

    
    
    
    path('travel/flights/', views.flight_home, name='flight_home'),
    path('travel/search/', views.flight_search, name='flight_search'),


    path('profile/', views.profile_page, name='profile'),

    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),

    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    path('submit_fashion_review/<int:product_id>/', views.submit_fashion_review, name='submit_fashion_review'),

    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),


    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('add_to_wishlist/<str:item_type>/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist/<int:wishlist_id>/', views.remove_wishlist, name='remove_wishlist'),


    path('chatbot/', views.chatbot_response, name='chatbot_response'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)