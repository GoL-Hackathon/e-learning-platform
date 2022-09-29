from django.shortcuts import render

# Create your views here.
def landingpage(request):
    return render(request, "landingpage.html")

def courses(request):
    return render(request, "courses.html")

def instructors(request):
    return render(request, "instructors.html")

def contact(request):
    return render(request, "contact.html")
