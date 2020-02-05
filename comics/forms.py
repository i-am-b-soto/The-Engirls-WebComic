from django import forms
from .models import ComicPanel, Tag
from dal import autocomplete

#Todo: Make this much more effecient
def getTagNames():
    return list (Tag.objects.values('text').distinct())

def getChapters():
    return list (ComicPanel.objects.values('chapter').distinct())


# The search form for the gallery
class ArchiveSearchForm(forms.Form):

    ascending = forms.BooleanField(required=False, label="Order by Newest first?")
    chapters = forms.ChoiceField(required = False, 
    	label ="Chapter", 
    	choices=getChapters(),  
    	widget = forms.Select(attrs = {
    		'id': 'chapterWidget',
    		'name':'chapter',
    		'class':'form-control'
    		}))

    # Auto complete on tag
    tag = autocomplete.Select2ListChoiceField(
        required=False,
        label="Tag:",
        choice_list=getTagNames(),
        widget=autocomplete.ListSelect2(
            url='comics/tag-autocomplete'))

