from django import forms 

from .models import Comment
#from dal import autocomplete


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
          'body': forms.Textarea(attrs={'rows':2, 'cols':20}),
        }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Say Something:" 


#Just use comment form for now
class ReplyForm(forms.ModelForm):
	body = forms.CharField(max_length = 3000, widget=forms.TextInput(attrs={'class':'reply_input_body'}))
	class Meta:
		model = Comment
		fields = ('body',)

	def __init__(self, *args, **kwargs):
		super(ReplyForm, self).__init__(*args, **kwargs)
		self.fields['body'].label = "" 