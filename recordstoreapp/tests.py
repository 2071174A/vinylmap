from django.test import TestCase
from django.core.urlresolvers import reverse
from recordstoreapp.models import Record, Store

class RecordMethodTests(TestCase):
    def test_ensure_title_is_not_empty_string(self):

        """
                ensure_title_is_not_empty_string should result True if the title is not an empty string
        """
        record = Record(title="Eclipse", artist="Twin Shadow")
        record.save()
        self.assertEqual((record.title!=" "), True)

class StoreMethodTests (TestCase):
    def test_ensure_store_has_link(self):
        store=Store(name= "RecordStore", link="www.recordstore.ac.uk")
        store.save()
        self.assertEqual((store.link!=" "), True)
