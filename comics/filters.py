import django_filters
from .models import ComicPanel
from django.conf import settings
from dal import autocomplete

"""
References:  

Filter references: https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter
github: https://github.com/carltongibson/django-filter
Adding choices: https://stackoverflow.com/questions/1455415/using-django-filter-with-choices-field-need-any-option

To get chapter and episode to be based off series: 
	https://stackoverflow.com/questions/49174420/how-to-filter-a-modelmultiplechoicefield-based-on-another-field

"""
def get_chapter_list(request):
	print("request: " + str(request))
	if not request:
		return []
	qs = ComicPanel.objects.all()
	series = request.GET.get('series', None)

	if series:
		qs = qs.filter(series = series)

	chapters_dicts = qs.values_list('chapter').distinct()
	chapters_list = []
	i = 0
	for item in chapters_dicts:
		chapters_list.append((item[0],item[0]))
		i = i+1
	if settings.DEBUG:
		print("WE'RE HERE!!!")
		
	return chapters_list


def getUniqueSeries():
	series_dicts = ComicPanel.objects.all().values_list('series').distinct()
	series_list = []
	i = 0
	for item in series_dicts:
		series_list.append((item[0],item[0]))
		if settings.DEBUG:
			pass
		i = i+1

	return series_list

def getUniqueChapters(series):
	chapters_list = []	
	if series:
		chapters_dicts = ComicPanel.objects.filter(series = series).values_list('chapter').distinct()
		i = 0
		for item in chapters_dicts:
			chapters_list.append((item[0], item[0]))
			i = i+1

	return chapters_list	

class ComicPanelFilter(django_filters.FilterSet):
	#chapter = NumberFilter(field_name='chapter', lookup_expr='gt')

	series = django_filters.ChoiceFilter(choices = getUniqueSeries)
	#chapter = django_filters.ChoiceFilter( )



	class Meta:
		model = ComicPanel
		fields = ['series', 'chapter', 'page']
		widgets = { 
		    'chapter': autocomplete.ListSelect2(url='/comics/auto_complete_chapter/', forward='series')
		}

	def __init__(self, *args, **kwargs):
		super(ComicPanelFilter, self).__init__(*args, **kwargs)
		print(self.request)
			
		#print(self.filters['series'].)
		#self.filters['chapter'].choices = getUniqueChapters(self.filters['series'].selected)