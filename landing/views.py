from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, "landing.html")

def pageslogin(request):
    return render (request, "pageslogin.html")

def pagesregister(request):
    return render (request, "pagesregister.html")


def usersprofile(request):
    return render(request, "usersprofile.html")



