from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import Record

# Create your views here.

# Home page
def index(request):
    context_dict = {}

    return render(request, 'index.html', context_dict)


#About page with description of tech used etc.
def about(request):
    context_dict = {}

    return render(request, 'about.html', context_dict)


#Email addresses or maybe a form to request a new item be added to the db.
def contact(request):
    context_dict = {}

    return render(request, 'contact.html', context_dict)


def search(request):
    return render(request, 'index.html', {})


def new_releases(request, genre_url='all'):
    context_dict = {}
    rec_list=Record.objects.order_by('-time')[:25]
    #context_dict['release_list'] = fetch_releases(genre_url, type)
    return render(request, 'releases.html', context_dict)
