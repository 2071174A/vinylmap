from django import forms
from recordstoreapp.models import Record,Store

class RecordForm(forms.ModelForm):
    title=forms.CharField(max_length=128,help_text="Record title: ")
    artist=forms.CharField(max_length=128,help_text="Artist name: ")
    label=forms.CharField(max_length=128,help_text="Label/Vendor: ")
    cat_no=forms.CharField(max_length=64,help_text="Catalogue number: ")
    genre=forms.CharField(max_length=64,help_text="Genre: ")
    class Meta:
        model=Record
        fields = ('title', 'artist', 'label', 'cat_no', 'genre')

class StoreForm(forms.ModelForm):
    link=forms.URLField(max_length=200,help_text="Store link:")
    price=forms.CharField(max_length=20,help_text="Price of record")
    name=forms.CharField(max_length=40,help_text="Store name")
    class Meta:
        model=Store
        fields = ('name', 'price', 'link')
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data