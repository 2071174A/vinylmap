from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import Genre

# Create your views here.

#Home page
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

#Used when one clicks a genre to get a genre-specific version of the front page.
def genre(request,genre_name_slug):
    if genre_name_slug is None:
        return HttpResponseRedirect('/')
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

def fetch_releases(genre_url, type='new'):
	release_list = []
	if genre_url == 'all':
		release_list = ['foobar']
		#fetch from all genres
		
	return release_list
	
def new_releases(request, genre_url='all'):
	context_dict = {}
	context_dict['release_list'] = fetch_releases(genre_url, type)
    
	return render(request, 'releases.html', context_dict)
	
def search(request):
	context_dict = {}
	#GET['q']

	return render(request, 'search.html', context_dict)

