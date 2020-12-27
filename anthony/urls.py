from django.urls import path
from .views import index, delete_city

urlpatterns = [
    path('delete_city/<str:city_name>', delete_city, name='delete_city'),
    path('', index, name='home'),
]
