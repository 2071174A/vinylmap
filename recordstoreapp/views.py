from django.shortcuts import render
from django.http import HttpResponse
from models import Genre

# Create your views here.

def index(request):
    return HttpResponse("index page")

def about(request):
    return HttpResponse("About page")

def genre(request,genre_name_slug):
    try:
        #note slugs are unique so this will return one row always
        genreTable = Genre.objects.get(slug=genre_name_slug)
    except Genre.DoesNotExist:
        return HttpResponse("Genre fail slug")
    return HttpResponse("genre page")

def backCat(request, genre_name_slug=None):
    context_dict = {}
    if genre_name_slug is None:
        return HttpResponse("Bottom level backCat")
    try:
        #note slugs are unique so this will return one row always
        genreTable = Genre.objects.get(slug=genre_name_slug)
    except Genre.DoesNotExist:
        return HttpResponse("Backcat genre fail slug")
    return HttpResponse("Backcat" + genreTable.name)

def forthcoming(request, genre_name_slug):
    return HttpResponse("forwardcat")

def newReleases(request, genre_name_slug):
    return HttpResponse("New Release page")

def contact(request):
    return HttpResponse("Contact Page")