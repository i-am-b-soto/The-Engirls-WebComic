from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Dynamic content for user 
class Content(models.Model):
	title = models.CharField(max_length=144, unique = True)
	body = RichTextUploadingField()
	position = models.IntegerField(help_text="Where your content is ordered in the nav bar", blank = True, null=True)

	class Meta:
		ordering = ('position',)

	def __str__(self):
		return "{}".format(str(self.title))