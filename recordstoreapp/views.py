from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import Record,Store
from django.db import connection
# Create your views here.

# Home page
def index(request):
    context_dict = {}

    return render(request, 'index.html', context_dict)

def about(request):
    context_dict = {}
    return render(request, 'about.html', context_dict)


#Email addresses or maybe a form to request a new item be added to the db.
def contact(request):
    context_dict = {}

    return render(request, 'contact.html', context_dict)


def search(request):
	context_dict = {}
	if 'q' in request.GET and request.GET['q'] != '':
		q = request.GET['q']
		cursor = connection.cursor()
		cursor.execute("SELECT id,title,artist FROM recordstoreapp_record WHERE title like '%" + q + "%' or artist like '%" + q + "%' or label like '%" + q + "%' or cat_no like '%" + q + "%';")
		rec_list=cursor.fetchall()
		
		total=len(rec_list)
		pg=int(request.GET['page']) if 'page' in request.GET else 1
		ub=min(pg*12, total)

		context_dict['rec_list'] = rec_list[(pg-1)*12:ub]
		context_dict['range'] = range(1,int(total/12)+1)
		context_dict['q'] = q

	return render(request, 'search.html', context_dict)


def new_releases(request):
	context_dict = {}
	
	rec_list = Record.objects.all()
	total=len(rec_list)
	pg=int(request.GET['page']) if 'page' in request.GET else 1
	ub=min(pg*12, total)

	context_dict['rec_list'] = rec_list[(pg-1)*12:ub]
	context_dict['range']=range(1,int(total/12)+1)

	return render(request, 'releases.html', context_dict)


def record_view(request):
    # context = RequestContext(request)
    page_id = None
    context_dict = {}
    if request.method == 'GET':
        if 'record_id' in request.GET:
            record_id = request.GET['record_id']
            if record_id:
                record = Record.objects.get(id=record_id)
                context_dict['stores']=Store.objects.filter(record=record)#record.stores.all()
                context_dict['rec'] = record
    return render(request, 'record.html', context_dict)
