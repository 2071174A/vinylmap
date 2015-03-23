import os

def populate():
	store1 = add_store(
                link="http://google.com",
                name="Google Records",
                price="$3.50")
	
        record1 = add_record(
                title="Record Title / Test Dub",
                artist="DJ wanka",
                cat_no="TEST001",
                label="Test Recordings",
                genre="Bionic Country Punk-Jazz",
                store=store1)

        recordStore_store = add_store(
                price = "20.99",
                link = "http://www.recordstore.co.uk/recordstore/Vinyl/Eclipse/497U02BS000",
                name = "RecordStore")

        test3_record = add_record(
                store = recordStore_store,
                title = "Eclipse",
                artist = "Twin Shadow",
                cat_no = "0093624930174",
                label = "Warner Bros",
                genre = "Jazz")
    
       

def add_store(link,name,price):
	s=Store(link=link,name=name,price=price)
	s.save()

def add_record(title,artist,cat_no,label,genre,store=None):
	r=Record(title=title,artist=artist,cat_no=cat_no,label=label,genre=genre)
	r.save()
	if store is not None:r.stores.add(store)

if __name__ == '__main__':
    print "Starting vinylmpas population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinylmap_project.settings')
    from recordstoreapp.models import Store, Record
    populate()


##from django.core.wsgi import get_wsgi_application
##os.environ['DJANGO_SETTINGS_MODULE'] = 'vinylmap_project.settings'
##application = get_wsgi_application()
##django.setup()
##from recordstoreapp.models import Record,Store
##populate()
