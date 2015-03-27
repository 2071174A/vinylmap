import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinylmap_project.settings')
import django
django.setup()

"""
Population script for testing purposes. For pulling real data from websites, run crawler.py instead.
"""
def populate():
	record1 = add_record(
		title="Record Title / Test Dub",
		artist="DJ wanka",
		cat_no="TEST001",
		label="Test Recordings",
		genre="Bionic Country Punk-Jazz"
		)
	store1 = add_store(
		link="http://google.com",
		name="Google Records",
		price="$3.50",
		record_obj=record1
		)
		
	test3_record = add_record(
		title = "Eclipse",
		artist = "Twin Shadow",
		cat_no = "0093624930174",
		label = "Warner Bros",
		genre = "Jazz"
		)
	recordStore_store = add_store(
		link = "http://www.recordstore.co.uk/recordstore/Vinyl/Eclipse/497U02BS000",
		name = "RecordStore",
		price = "20.99",
		record_obj=test3_record
		)

def add_store(link, name, price, record_obj):
	store=Store(link=link,name=name,price=price)
	store.save()
	record_obj.stores.add(store)
	
	return store

def add_record(title,artist,cat_no,label,genre,store=None):
	record=Record(title=title,artist=artist,cat_no=cat_no,label=label,genre=genre)
	record.save()
	if store is not None:
		record.stores.add(store)
	
	return record
	

if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinylmap_project.settings')
    from recordstoreapp.models import Store, Record
    populate()
