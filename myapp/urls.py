from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('ads.txt', views.ads),
		
]