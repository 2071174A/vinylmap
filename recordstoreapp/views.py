from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import Genre

# Create your views here.

def baseRedirect(request):
    return HttpResponseRedirect('/vinylmaps/')

#Home page
def index(request):
    return HttpResponse("index page")

#About page with description of tech used etc.
def about(request):
    return HttpResponse("About page")

#Email addresses or maybe a form to request a new item be added to the db.
def contact(request):
    return HttpResponse("Contact Page")

#Used when one clicks a genre to get a genre-specific version of the front page.
def genre(request,genre_name_slug):
    if genre_name_slug is None:
        return HttpResponseRedirect('/vinylmaps/')
    try:
        #note slugs are unique so this will return one row always
        genreTable = Genre.objects.get(slug=genre_name_slug)
    except Genre.DoesNotExist:
        return HttpResponse("Genre fail slug")
    return HttpResponse("genre page for " + genreTable.name)

# genre slug argument for if one reaches the page through the sidebar
def backCat(request, genre_name_slug=None):
    context_dict = {}
    if genre_name_slug is None:
        return HttpResponseRedirect('/vinylmaps/') #behaviour for default backcat,
        # redirects home since only forward and new are usable w.o. genre
    try:
        #slugs are set to be unique so this will return one row always
        genreTable = Genre.objects.get(slug=genre_name_slug)
    except Genre.DoesNotExist:
        return HttpResponseNotFound('<h1>Genre \"' + genre_name_slug + '\" not found</h1>')

    return HttpResponse(genreTable.name + " genre's backcatalogue page") #redirect to basic backCat


def forthcoming(request, genre_name_slug):
    context_dict = {}
    if genre_name_slug is None:
        return HttpResponse("Bottom level backCat")
    try:
        genreTable = Genre.objects.get(slug=genre_name_slug)
    except Genre.DoesNotExist:
        return HttpResponse("Forward genre fail slug")
    return HttpResponse("Forwardcat" + genreTable.name)


def newReleases(request, genre_name_slug):
    return HttpResponse("New Release page")

