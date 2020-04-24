from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import os
from io import StringIO,BytesIO
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.conf import settings
from .url_changer import change_url
from .CropImage import cropped_thumbnail
import _thread as thread
from subscriptions.utils import send_new_comic_email

"""
	Return: 
		str Name of the main series 
"""
def getMainSeriesName():
	return settings.MAIN_SERIES_NAME

"""
	Comic Panel Object  
"""
class ComicPanel(models.Model):

	# Title of our comic/ youtube video
	title = models.CharField(max_length = 255)	

	# User uploaded image for the comic/youtube video (If a youtube video this image will be used for the thumbnail)
	image = models.ImageField(upload_to = 'comics/') 
	
	# The youtube URL (optional)
	youtube_url = models.URLField(max_length=250, null = True, blank = True, help_text = "Insert a Youtube URL if you want a video for a comic")
	
	# Our description 
	description = RichTextUploadingField()

	# Custom Caption 
	caption = models.CharField(max_length = 500)

	# Series, defaults to settings.MAIN_SERIES_NAME
	series = models.CharField(max_length = 255, null = False, blank = False, default = getMainSeriesName, 
		help_text="The default value is what the main Series Name is set to in Settings.py" )

	# Chapter, optional
	chapter = models.FloatField(null = True, blank = True)

	# page, optional
	page = models.IntegerField(null = True, blank = True, name="page")

	# Send emails? 
	send_emails = models.BooleanField(default= True)

	# Time of upload
	uploadTime = models.DateField(default=timezone.now)

	# Thumbnail of the picture
	thumbnail = models.ImageField(
		upload_to='comics/thumbnails/',
		null=True,
		blank=True)  # the small 200x200 picture object   

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['series','chapter', 'page'], name='Must be null or unique')
			]

	def __str__(self):
		return self.title


	"""
		Generates Thumbnail. Saves in Media location /thumbnails
	"""
	def generateThumbnail(self):
			
		if self.image.name.endswith(".jpg"):
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
			DJANGO_TYPE = 'image/jpeg'

		elif self.image.name.endswith(".png"):
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'
			DJANGO_TYPE = 'image/png'

		instance = self.image

		try:
			instance.open()
		except Exception as e:
			print("Error opening instance image")
			return
		# Open original photo which we want to thumbnail using PIL's Image

		try:
			image = Image.open(BytesIO(instance.read()))
		except IOError as e:
			print("Error opening in memory file: " + str(e))
			return

		# Crop out 1/4 the larger dimension of the image
		if image.height >= image.width:
			image = image.crop( tuple( (0, 0, int(round(image.width)), int(round(image.height-image.height/4)))) )
		elif image.width > image.height:
			image = image.crop( tuple( (0, 0 , int(round(image.width - image.width/4)), int(round(image.height)))) )

		# Send the cropped image to be resized to the sandard thumbnail size
		image = cropped_thumbnail(image)

		# Save the thumbnail
		temp_handle = BytesIO()
		try:
			image.save(temp_handle, PIL_TYPE)
		except KeyError as e:
			print("Error when saving in memory file " + str(e))
			return
		except IOError as e:
			print("Error when saving in memory file " + str(e))
			return

		if settings.DEBUG:
			print("Successfully saved in memory thumbnail")

		try:
			temp_handle.seek(0)
		except EOFError as e:
			print("Error when seeking in memory file: " + str(e))

		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		try:
			suf = SimpleUploadedFile(os.path.split(instance.name)[-1],
					temp_handle.read(), content_type=DJANGO_TYPE)
		except FileNotFoundError:
			if settings.DEBUG:
				print("Error in simple file upload")
				return
		except Exception: 
			print("Error while creating thumbnail")
			return

		try:
			# Save SimpleUploadedFile into image field
			self.thumbnail.save(
				'%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
				suf,
				save=False
			)
		except exception as e:
			print("Error saving thumbnail file to image field" + str(e))
			return

	"""
		Save -
		1) Generate Thumbnail
		2) Generate youtube_url (if any)
		3) Send emails
	"""
	def save(self):
		#self.set_thumbnail_resize()
		self.generateThumbnail()
		self.youtube_url = change_url(self.youtube_url)

		if self.send_emails:
			try:
				thread.start_new_thread( send_new_comic_email,  (self.title, ) )
			except Exception as e:
				print("Unable to start new thread-{}\n Unable to send emails".format(str(e)))

		#self.image.open()
		super(ComicPanel, self).save()


