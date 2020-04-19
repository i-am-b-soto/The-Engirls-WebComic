from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from subscriptions.utils import send_new_post_email
import _thread as thread

"""
	Post model
"""
class Post(models.Model):
	
	# The title of the blog
	title = models.CharField(max_length=144, blank=False, null=False)
	
	# The text of the blog, as a rich editor
	body = RichTextUploadingField()
	
	# Created on Date
	created_on = models.DateField(default=timezone.now)
	
	# What category is the blog in?
	category = models.CharField(max_length=144, blank=True, null=True)

	# Send emails? 
	send_emails = models.BooleanField(default= True)

	class Meta:
		ordering = ('-created_on',)

	def __str__(self):
		return self.title

	"""
		Save 
			send emails
	"""
	def save(self):
		if self.send_emails:
			try:
				thread.start_new_thread( send_new_post_email,  (self.title, ) )
			except Exception as e:
				print("Unable to start new thread-{}\n Unable to send emails".format(str(e)))

		super(Post, self).save()	



