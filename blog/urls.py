from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="BlogHome"),
     path('blogpos/<int:id>', views.blogpost, name="BlogPost"),
]