from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home(request):
    return HttpResponse("Hello world. This is a placeholder until something is written.")

# Create your views here.
