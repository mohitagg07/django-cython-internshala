# ecom_project/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- 1. Add 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # <-- 2. Add this line
]