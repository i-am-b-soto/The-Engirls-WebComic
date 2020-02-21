from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# In future projects this should really be its own app
class Post(models.Model):
	title = models.CharField(max_length=144, blank=False, null=False)
	body = RichTextUploadingField()
	created_on = models.DateField(default=timezone.now)
	category = models.CharField(max_length=144, blank=True, null=True)

	def __str__(self):
		return self.title	

# in future projects this should really be its own app
class Comment(models.Model):
	Post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name = models.CharField(max_length=144, blank=True, null=True)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)


