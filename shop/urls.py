
from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about/' ,views.about, name="AboutUS"),
    path('contact/', views.contact, name="contactUS"),
    path('search/', views.search, name="search"),
    path('checkout/', views.checkout, name="checkout"),
    path('prodview/<int:myid>', views.prodview, name="prodview"),
    path('tracker/', views.tracker, name="tracker"),
]
