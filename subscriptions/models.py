from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Subscription Model
class Subscription(models.Model):
    email = models.EmailField(blank = False, null = False, unique = True)
    key = models.CharField(max_length= 11, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return 'Email: {} key: {} created on: {}'.format(self.email, self.key, str(self.created_on))

class CustomEmail(models.Model):
	subject = models.CharField(max_length=255)
	body = RichTextUploadingField()