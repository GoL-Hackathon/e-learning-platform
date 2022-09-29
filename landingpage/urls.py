from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("courses/", views.courses, name="courses"),
    path("instructors/", views.instructors, name="instructors"),
    path("contact/", views.contact, name="contact"),

]
