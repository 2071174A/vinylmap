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