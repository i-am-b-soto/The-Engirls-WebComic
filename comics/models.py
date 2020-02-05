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
	chapter = models.FloatField(null = True, blank = True)
	episode = models.IntegerField(null = True, blank = True)
	#chapter = models.FloatField(null=True, validators=[MinValueValidator(1)])
	#episode = models.IntegerField(null=True, validators=[MinValueValidator(1)])

	#TODO Twitter + Instagram Feeds
	# Time of upload
	uploadTime = models.DateField(default=timezone.now)

	# (width, height) of thumbnail
	_thumbnail_size = (241, 200)
	# Thumbnail of the picture
	thumbnail = models.ImageField(
		upload_to='thumbnails/',
		null=True,
		blank=True)  # the small 200x200 picture object   

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['chapter', 'episode'], name='Must be null or unique')
			]

	def __str__(self):
		return self.title

	def _get_inner_crop_dimens(self, image):
		'''Return tuple of dimensions for inner crop of thumnail image.'''

		# Get dimensions of image
		image_width, image_height = image.size

		# Check if image size is unreasonable
		# TODO: See if this error check can be tossed
		if image_width < int(self._thumbnail_size[0]) \
			or image_height < int(self._thumbnail_size[1]):
			return (0, 0, 5, 5)

		# Get image center point
		image_center_width = image_width / 2
		image_center_height = image_height /2

		# Get origin and end point of crop
		origin_x = image_center_width - int(self._thumbnail_size[0] / 2)
		origin_y = image_center_height - int(self._thumbnail_size[1] / 2)
		end_x = origin_x + int(self._thumbnail_size[0])
		end_y = origin_y + int(self._thumbnail_size[1])

		# Final dimensions of crop
		crop_dimens = (origin_x, origin_y, end_x, end_y)
		#print "crop dimens: " + ','.join([str(cd) for cd in crop_dimens])

		return crop_dimens	

	def generateThumbnail(self):
		'''Generate a center-zoom square thumbnail of original image.'''

		mode =''
		pixelColorValues = None

		# See what kind of file we are dealing with
		if self.image.name.endswith('.jpg'):
			pilImageType = 'jpeg'
			fileExtension = 'jpg'
			djangoType = 'image/jpeg'
			mode = 'RGB'
			pixelColorValues = (255,255,255)
		elif self.image.name.endswith(".png"):
			pilImageType = "png"
			fileExtension = "png"
			djangoType = 'image/png'
			mode = 'RGBA'
			pixelColorValues = (255,255,255,0)

		# Open big picture into PIL
		self.image.seek(0)
		OriginalImage = Image.open(BytesIO(self.image.read()))
		#python 2 code -
		#OriginalImage = Image.open(StringIO(self.image.read()))

		# Crop image
		inner_crop_dimens = self._get_inner_crop_dimens(OriginalImage)
		OriginalImage = OriginalImage.crop(inner_crop_dimens)
		#OriginalImage.thumbnail(thumbnailSize, Image.ANTIALIAS)

		# Save image
		tempHandle = BytesIO()

		#print("Original image: " + OriginalImage)

		# Original Python 2 code
		#tempHandle = StringIO()
		background = Image.new(mode, self._thumbnail_size, pixelColorValues)
		background.paste(OriginalImage,( (int(self._thumbnail_size[0]) - int(OriginalImage.size[0] / 2)), (int(self._thumbnail_size[1]) - int(OriginalImage.size[1] / 2))))
		background.save(tempHandle, pilImageType)
		tempHandle.seek(0)
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], tempHandle.read(), content_type=djangoType)
		self.thumbnail.save('%s.%s' % (os.path.splitext(suf.name)[0], fileExtension), suf, save=False)
	   
	def save(self):
		self.generateThumbnail()


		super(ComicPanel, self).save()

class Tag(models.Model):
	picture = models.ForeignKey(ComicPanel, on_delete = models.CASCADE)
	tag = models.CharField(max_length=15, null=False)

