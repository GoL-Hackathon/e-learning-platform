from django.urls import path
from .import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path('pageslogin/', views.pageslogin, name='pageslogin'),
    path('pagesregister/', views.pagesregister, name='pagesregister'),
    path('usersprofile/', views.usersprofile, name='usersprofile'),

]

