from django import forms
#from .models import ComicPanel
from dal import autocomplete

#Todo: Make this much more effecient
def getSeriesNames():
    pass
    #return list (ComicPanel.objects.values('series_name').distinct())

def getChapters():
    pass
    #return list (ComicPanel.objects.values('chapter').distinct())


# The search form for the gallery
class ArchiveSearchForm(forms.Form):

    ascending = forms.BooleanField(required=False, label="Order by Newest first?")
    
    """
    TODO: Filter by chapter
    chapters = forms.ChoiceField(
        required = False, 
    	label ="Chapter:", 
    	choices=getChapters(),  
    	widget = forms.Select(attrs = {
    		'id': 'chapterWidget',
    		'name':'chapter',
    		'class':'form-control'
    		}))
    """

    # Auto complete on tag
    series = autocomplete.Select2ListChoiceField(
        required=False,
        label="Series:",
        choice_list=getSeriesNames(),
        widget=autocomplete.ListSelect2(
            url='comics/series-autocomplete'))

