import django_filters
from .models import Post

def getUniqueCategory():
	category_dicts = Post.objects.all().values_list('category').distinct()
	category_list = []
	i = 0
	for item in category_dicts:
		category_list.append((item[0],item[0]))
		i = i+1

	return category_list

class PostFilter(django_filters.FilterSet):
	#chapter = NumberFilter(field_name='chapter', lookup_expr='gt')

	category = django_filters.ChoiceFilter(choices = getUniqueCategory)
	# The following does not have the intended resulrs; options in the form of: ('main',), ('None',)... etc
	#series=django_filters.ModelChoiceFilter(queryset=ComicPanel.objects.all().values_list('series').distinct())



	class Meta:
		model = Post
		fields = ['category']