from django.db import models
from ckeditor.fields import RichTextField
#from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from PIL import Image
import os
from io import StringIO,BytesIO
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

#TODO Add validation in the admin form to makesure chapter, episode is not repeated


# Create your models here.
class ComicPanel(models.Model):

	title = models.CharField(max_length = 255)
	image = models.ImageField(upload_to = 'comics/')
	#TODO, Change this if approperiate
	description = RichTextField()
	caption = models.CharField(max_length = 500)


	series = models.CharField(max_length = 255, null = False, blank = False, default = "main", help_text="Label the series as main to be the default comic series" )
	chapter = models.FloatField(null = True, blank = True)
	episode = models.IntegerField(null = True, blank = True)
	#chapter = models.FloatField(null=True, validators=[MinValueValidator(1)])
	#episode = models.IntegerField(null=True, validators=[MinValueValidator(1)])

	#TODO Twitter + Instagram Feeds
	# Time of upload
	uploadTime = models.DateField(default=timezone.now)

	# (width, height) of thumbnail
	_thumbnail_size = (150, 100)
	# Thumbnail of the picture
	thumbnail = models.ImageField(
		upload_to='comics/thumbnails/',
		null=True,
		blank=True)  # the small 200x200 picture object   

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['series','chapter', 'episode'], name='Must be null or unique')
			]

	def __str__(self):
		return self.title




	def generateThumbnail(self):
		'''Generate a center-zoom square thumbnail of original image.'''
		# Original code: https://gist.github.com/valberg/2429288

	  # Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = self._thumbnail_size

		DJANGO_TYPE = self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'

		# Open original photo which we want to thumbnail using PIL's Image
		image = Image.open(StringIO(self.image.read()))

		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

		# Save the thumbnail
		temp_handle = ByteIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)

		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
				temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save(
			'%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
			suf,
			save=False
		)

	def save(self):
		self.generateThumbnail()


		super(ComicPanel, self).save()