from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Dynamic content for user 
class Content(models.Model):
	title = models.CharField(max_length=144, blank=False, null=False)
	body = RichTextUploadingField()
	position = models.IntegerField(help_text="Where your content is ordered in the nav bar")

	class Meta:
		ordering = ('position',)

	def __str__(self):
		return "{}".format(str(self.title))