from django import forms
from .models import Comment, ComicPanel
#from dal import autocomplete


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


#Todo: Make this much more effecient
def getSeriesNames(series_index=-1):
    if series_index == 0:
        return None

    the_list = list (ComicPanel.objects.values('series').distinct())
    x = 1
    tuple_list = []
    tuple_list.append((0, ''))
    for item in the_list:
        if series_index == str(x):
            return item['series']        
        tuple_list.append((x,item['series']))
        x = x + 1


    return tuple_list

def getChapters():
    pass
    #return list (ComicPanel.objects.values('chapter').distinct())


# The search form for the gallery
class ArchiveSearchForm(forms.Form):

    ascending = forms.BooleanField(required=False, label="Order by Newest first?")
    
    

      #TODO: Filter by chapter
 #   chapters = forms.ChoiceField(
 #       required = False, 
 #      label ="Chapter:", 
 #      choices=getChapters(),  
 #      widget = forms.Select(attrs = {
 #          'id': 'chapterWidget',
 #          'name':'chapter',
 #          'class':'form-control'
 #          }))  

    # Auto complete on tag
    series = forms.ChoiceField(
        required=False,
        label="Series:",
        choices= getSeriesNames())

