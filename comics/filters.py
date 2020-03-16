import django_filters
from .models import ComicPanel
from django.conf import settings
from dal import autocomplete
from django import forms 

"""
References:  

Filter references: https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter
github: https://github.com/carltongibson/django-filter
Adding choices: https://stackoverflow.com/questions/1455415/using-django-filter-with-choices-field-need-any-option

To get chapter and episode to be based off series: 
	https://stackoverflow.com/questions/49174420/how-to-filter-a-modelmultiplechoicefield-based-on-another-field


Attempting to make the filters look beautiful. If successful answer this Stack overflow question:
https://stackoverflow.com/questions/28961056/adding-external-widget-to-django-filters


"""


def getUniqueSeries():
	series_dicts = ComicPanel.objects.all().values_list('series').distinct()
	return [(item[0], item[0]) for item in series_dicts]

def getUniqueChapters():
	chapters_dicts = ComicPanel.objects.all().values_list('chapter').distinct()
	return [(item[0], item[0]) for item in chapters_dicts]

def getUniquePages():
	pages_dicts = ComicPanel.objects.all().values_list('page').distinct()
	return [(item[0],item[0]) for item in pages_dicts]		

class ComicPanelFilter(django_filters.FilterSet):
	#chapter = NumberFilter(field_name='chapter', lookup_expr='gt')

	series = django_filters.ChoiceFilter(choices = getUniqueSeries, widget=forms.Select(attrs={}) )
	#chapter = django_filters.ChoiceFilter(widget = autocomplete.ListSelect2(url='/comics/auto_complete_chapter/', forward='series') )
	chapter = django_filters.ChoiceFilter( choices = getUniqueChapters , widget=forms.Select(attrs={}))
	page = django_filters.ChoiceFilter(choices = getUniquePages , widget=forms.Select(attrs={}))

	class Meta:
		model = ComicPanel
		fields = ['series', 'chapter', 'page']



	def __init__(self, *args, **kwargs):
		super(ComicPanelFilter, self).__init__(*args, **kwargs)
		#print(self.request)
			
		#print(self.filters['series'].)
		#self.filters['series'].label = ""