from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

#genre table holds the slugs for URL mapping and their names for
#display
class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    artistID = models.IntegerField(default = 0, unique = True)
    names = models.CharField(max_length=128)
    biography = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.artistID


class Record(models.Model):
    recordID = models.IntegerField(default=0, unique=True)
    catalogueNum = models.IntegerField(default=0)
    names = models.CharField(max_length=128)
    tracks = models.CharField(max_length = 128)
    picture = models.ImageField()
    genre = models.CharField(max_length = 128)
    releaseDate = models.DateField()

    def __unicode__(self):
        return self.recordID

class Label(models.Model):
    labelID = models.IntegerField(default = 0, unique=True)
    name = models.CharField(max_length=128)
    bio = models.CharField(max_length = 128)
        
    def __unicode__(self):
        return self.labelID

class RecordStore(models.Model):
    record = models.ForeignKey(Record)
    link = models.URLField()       

    def __unicode__(self):
        return self.record
