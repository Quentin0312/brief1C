from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def mainDashboard(request):

    return HttpResponse("hello world")