from django.contrib.sitemaps import Sitemap
from recordstoreapp.models import *

class RecordMap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Record.objects.all()

    def lastmod(self, obj):
        return obj.pub_date