from django.db import models

# Create your models here.

class Store(models.Model):
    price=models.CharField(max_length=40,default='')
    link=models.URLField(blank=True)
    def __unicode__(self):
        return self.link


class Record(models.Model):
    title=models.CharField(max_length=128,default='')
    artist=models.CharField(max_length=128,default='')
    cover=models.CharField(max_length=128,default='')
    cat_no=models.CharField(max_length=64,default='')
    label=models.CharField(max_length=128,default='')
    genre=models.CharField(max_length=64,default='')
    time=models.DateTimeField(auto_now=True)
    stores=models.ManyToManyField(Store)
    def __unicode__(self):
        return self.title




