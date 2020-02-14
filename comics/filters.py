import django_filters
from .models import ComicPanel

class ComicPanelFilter(django_filters.FilterSet):
	#chapter = NumberFilter(field_name='chapter', lookup_expr='gt')
    class Meta:
        model = ComicPanel
        fields = ['series', 'chapter', 'episode']