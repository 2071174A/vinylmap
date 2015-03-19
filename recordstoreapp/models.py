from django.db import models

# Create your models here.

class Store(models.Model):
    price=models.FloatField(default=0.0)
    link=models.URLField(blank=True)
    def __unicode__(self):
        return self.link


class Record(models.Model):
    title=models.CharField(max_length=128)
    artist=models.CharField(max_length=128)
    cover=models.CharField(max_length=128)
    cat_no=models.CharField(max_length=64,unique=True)
    label=models.CharField(max_length=128)
    genre=models.CharField(max_length=64)
    time=models.DateTimeField(auto_now=True)
    stores=models.ManyToManyField(Store)
    def __unicode__(self):
        return self.title




