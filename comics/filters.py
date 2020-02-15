import django_filters
from .models import ComicPanel

"""
References:  

Filter references: https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter
github: https://github.com/carltongibson/django-filter
Adding choices: https://stackoverflow.com/questions/1455415/using-django-filter-with-choices-field-need-any-option

"""
def getUniqueSeries():
	series_dicts = ComicPanel.objects.all().values_list('series').distinct()
	series_list = []
	i = 0
	for item in series_dicts:
		series_list.append((i,item[0]))
		i = i+1
	return series_list

class ComicPanelFilter(django_filters.FilterSet):
	#chapter = NumberFilter(field_name='chapter', lookup_expr='gt')

	series = django_filters.ChoiceFilter(choices = getUniqueSeries())
	# The following does not have the intended resulrs; options in the form of: ('main',), ('None',)... etc
	#series=django_filters.ModelChoiceFilter(queryset=ComicPanel.objects.all().values_list('series').distinct())



	class Meta:
		model = ComicPanel
		fields = ['chapter', 'episode']

