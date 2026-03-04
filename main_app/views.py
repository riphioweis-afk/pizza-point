
from django.shortcuts import render

# Import HttpResponse to send text-based responses
from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('Pizza Point Home Page')
def kitchen(request):
    return render(request, 'kitchen.html')