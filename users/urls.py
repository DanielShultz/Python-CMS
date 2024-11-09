from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.staff, name='staff'),
    path('author/<str:username>', views.author, name='author'),
]