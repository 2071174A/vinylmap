from django import forms
from recordstoreapp.models import Record

class RecordForm(forms.ModelForm):
	title = forms.CharField(max_length=32, help_text="Please enter the record title.")
	artist = forms.CharField(max_length=32, help_text="Please enter the artist.")
	url = forms.URLField(max_length=200, help_text="Please enter the store URL of the record.")
	cover = forms.URLField(max_length=200, help_text="Please enter the cover URL of the record.")
	label =  forms.CharField(max_length=32, help_text="Please enter the label name.")
	cat_no = forms.CharField(max_length=32, help_text="Please enter the catalogue number.")
	price = forms.CharField(max_length=32, help_text="Please enter the price of the record.")
	
	class Meta:
		# Provide an association between the ModelForm and a model
		model = Record

		# What fields do we want to include in our form?
		# This way we don't need every field in the model present.
		# Some fields may allow NULL values, so we may not want to include them...
		# Here, we are hiding the foreign key.
		fields = ('title', 'artist', 'url', 'cover', 'label', 'cat_no', 'price')
		
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		# If url is not empty and doesn't start with 'http://', prepend 'http://'.
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data