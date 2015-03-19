from django.contrib import admin

# Register your models here.
from django.contrib import admin
from recordstoreapp.models import Record

# Add in this class to customized the Admin Interface
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Update the registeration to include this customised interface
admin.site.register(Record)


