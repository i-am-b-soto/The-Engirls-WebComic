from django import forms 

from .models import Comment, Post
#from dal import autocomplete


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
          'body': forms.Textarea(attrs={'rows':3, 'cols':40}),
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Comment:" 
