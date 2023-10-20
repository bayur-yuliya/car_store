from django.http import HttpResponse
from django.shortcuts import render


def cars(request):
    return HttpResponse("Cars")
