from django.conf import settings 
from .models import Content 
from django.template.loader import render_to_string
from django import template
#from django.template.loader.exceptions import TemplateDoesNotExist


"""
	Load the default content based of CONTENT_KEY_NAMES in settings

	Things to consider:
		1) If title already exists in contents, don't load it
		2) If the default html file cannot be found, dont load content, 
		   but don't throw exception
"""
def load_default_content():
	# Iterate over the content names in settings
	for content_name in settings.CONTENT_KEY_NAMES.values():

		# Do we already have something twith this title name?
		if not Content.objects.filter(title = content_name).exists():
			# The default html name will be lowercase(content_name)_default.html 
			html_name = "{}_default.html".format(content_name.lower())
			try:
				html = render_to_string(html_name)
			except template.TemplateDoesNotExist:
				print("{} Does not exist".format(html_name))
				html = "Create your own Content with an html file named {}".format(html_name)

			key_content = Content.objects.create(title = content_name, body = html, position = 0)
			key_content.save()
			print("{} Created".format(key_content.title))
		else:
			print("{} already exists.".format(content_name))
