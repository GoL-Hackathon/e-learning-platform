from django.http import JsonResponse
from django.shortcuts import render

from .email import send_welcome_email
from .forms import NewsLetterForm
from .models import NewsLetterRecipients


# Create your views here.
def landingpage(request):
    form = NewsLetterForm()
    return render(request, "landingpage.html", {'form': form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient =  NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

def courses(request):
    return render(request, "courses.html")

def instructors(request):
    return render(request, "instructors.html")

def contact(request):
    return render(request, "contact.html")
