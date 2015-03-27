from django.test import TestCase
from django.core.urlresolvers import reverse
from recordstoreapp.models import Record, Store
import populate

class RecordMethodTests(TestCase):
    def test_ensure_title_is_not_empty_string(self):
        """
                ensure_title_is_not_empty_string should result True if the title is not an empty string
        """
        record = Record(title="Eclipse", artist="Twin Shadow")
        record.save()
        self.assertEqual((record.title!=" "), True)

    def test_ensure_artist_exists(self):
        """
               test_ensure_artist_exists should result True if there is artist present
        """
        record = Record(title="Moon", artist="Clark")
        record.save()
        self.assertEqual ((record.artist!=""), True)


class StoreMethodTests (TestCase):
    def test_ensure_store_has_link(self):
        """
                test_ensure_store_has_link should result True if there's is a link
        """
        
        store=Store(name= "RecordStore", link="www.recordstore.ac.uk")
        store.save()
        self.assertEqual((store.link!=" "), True)


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
                test that invalid record requests pull the 404 page

        """
        response = self.client.get("/records/?record_id=-1")
        self.assertContains(response, "Http Error 404")

class NewReleasesTest(TestCase):
    def test_new_releases_exist(self):
        """
                checks if the added record is in the new_releases page
        """
        populate.add_record(title = "Eclipse",
		artist = "Twin Shadow",
		cat_no = "0093624930174",
		label = "Warner Bros",
		genre = "Jazz"
		)
        response = self.client.get(reverse('new_releases'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eclipse")


class AddRecordTest(TestCase):
    def test_cat_no_matches(self):
        """
                checks if the added cat_no is the cat_no in the website
        """
        record1 = populate.add_record(title = "Eclipse",
		artist = "Twin Shadow",
		cat_no = "0093624930174",
		label = "Warner Bros",
		genre = "Jazz"
		)
        response = self.client.get('/records/?record_id='+ str(record1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"0093624930174")
        

        
    
