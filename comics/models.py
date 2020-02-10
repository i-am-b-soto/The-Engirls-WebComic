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
from django.conf import settings

#TODO Add validation in the admin form to makesure chapter, episode is not repeated

def getMainSeriesName():
	return settings.MAIN_SERIES_NAME

# Create your models here.
class ComicPanel(models.Model):

	title = models.CharField(max_length = 255)
	image = models.ImageField(upload_to = 'comics/')
	#TODO, Change this if approperiate
	description = RichTextField()
	caption = models.CharField(max_length = 500)


	series = models.CharField(max_length = 255, null = False, blank = False, default = getMainSeriesName, 
		help_text="The default value is what the main Series Name is set to in Settings.py" )
	chapter = models.FloatField(null = True, blank = True)
	episode = models.IntegerField(null = True, blank = True)
	#chapter = models.FloatField(null=True, validators=[MinValueValidator(1)])
	#episode = models.IntegerField(null=True, validators=[MinValueValidator(1)])

	#TODO Twitter + Instagram Feeds
	# Time of upload
	uploadTime = models.DateField(default=timezone.now)


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


	def getThumnbnailSize(self, division_fact):
		# length > width? Should be
		

		# If height is larger. Given width = width/4, what is height?
		if self.image.width < self.image.height:
			# Percentage difference
			pct_diff = (self.image.height - self.image.width) / self.image.height
			newheight = ((self.image.width / division_fact) * pct_diff) + (self.image.width/division_fact) 
			
			return (self.image.width/division_fact, newheight)

		# width is larger . Given height = height/4, what is width
		elif self.image.width > self.image.height: 
			pct_diff = (self.image.width - (self.image.height/division_fact)) / self.image.width
			newwidth = (self.image.height/division_fact) * pct_diff + (self.image.height/division_fact)

			return (newwidth, self.image.height/division_fact)

	def generateThumbnail(self):
		'''Generate a center-zoom square thumbnail of original image.'''
		# Original code: https://gist.github.com/valberg/2429288

	  # Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = self.getThumnbnailSize(division_fact = 3)

		if settings.DEBUG:
			print("Thumbnail size: ")
			print(THUMBNAIL_SIZE)
		#DJANGO_TYPE = self.image.file.content_type

		if self.image.name.endswith(".jpg"):
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
			DJANGO_TYPE = 'image/jpeg'

		elif self.image.name.endswith(".png"):
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'
			DJANGO_TYPE = 'image/png'

			instance = self.image
			instance.open()
			# Open original photo which we want to thumbnail using PIL's Image
			image = Image.open(BytesIO(instance.read()))

			# We use our PIL Image object to create the thumbnail, which already
			# has a thumbnail() convenience method that contrains proportions.
			# Additionally, we use Image.ANTIALIAS to make the image look better.
			# Without antialiasing the image pattern artifacts may result.
			image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

			# Save the thumbnail
			temp_handle = BytesIO()
			image.save(temp_handle, PIL_TYPE)
			temp_handle.seek(0)

			# Save image to a SimpleUploadedFile which can be saved into
			# ImageField
			try:
				suf = SimpleUploadedFile(os.path.split(instance.name)[-1],
						temp_handle.read(), content_type=DJANGO_TYPE)
			except FileNotFoundError:
				if settings.DEBUG:
					print("Error in simple file upload")
			except Exception: 
				print("Error while creating thumbnail")


			if settings.DEBUG:
				print("suf:")
				print(suf.name)
				
			# Save SimpleUploadedFile into image field
			self.thumbnail.save(
				'%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
				suf,
				save=False
			)


		

	def save(self):
		#self.set_thumbnail_resize()
		self.generateThumbnail()
		#self.image.open()
		super(ComicPanel, self).save()