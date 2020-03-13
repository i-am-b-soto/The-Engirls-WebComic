from django.db import models
from django.utils import timezone
from comics import models as comics_models
from blog import models as blog_models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Comment(models.Model):
    ComicPanel = models.ForeignKey(comics_models.ComicPanel ,on_delete=models.CASCADE, related_name='comic_panel_comments', blank = True, null = True)
    Post = models.ForeignKey(blog_models.Post, on_delete=models.CASCADE, related_name ='post_comments', blank = True, null = True)
    Comment = models.ForeignKey("self", on_delete=models.CASCADE, related_name = 'comment_comments', blank =True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE) 
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add = True, null = True)

    class Meta:
        ordering = ('-updated_on', '-created_on')

    #Reference: https://stackoverflow.com/questions/53085645/django-one-of-2-fields-must-not-be-null
    #def clean(self):
    #	super().clean()
    #	if self.ComicPanel is None and self.Post is None and self.Comment is None:
    #		raise ValidationError('Comment must have reference to either a post, a comic, or another comment')


    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Comment_Like(models.Model):
	Comment = models.ForeignKey('Comment', on_delete = models.CASCADE, related_name = 'likes')
	count = models.IntegerField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 