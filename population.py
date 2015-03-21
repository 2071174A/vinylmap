
def populate():
	pass

def add_store(link,name,price):
	s=Store(link=link,name=name,price=price)
	store.save()

def add_record(title,artist,cat_no,label,genre,store=None):
	r=Record(title=title,artist=artist,cat_no=cat_no,label=label,genre=genre)
	r.save()
	if store is not None:r.stores.add(store)

store1 = add_store(
	link="http://google.com",
	name="Google Records",
	price="$3.50",
)
	
record1 = add_page(
	title="Record Title / Test Dub",
	artist="DJ wanka",
	cat_no="TEST001",
	label="Test Recordings",
	genre="Bionic Country Punk-Jazz",
	url="http://google.com",
	store=store1,
	)

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'vinylmap_project.settings'
application = get_wsgi_application()
django.setup()
from recordstoreapp.models import Record,Store
populate()