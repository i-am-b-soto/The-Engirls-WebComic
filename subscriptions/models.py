from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import _thread as thread

""" 
	Subscription Model

"""
class Subscription(models.Model):

    email = models.EmailField(blank = False, null = False, unique = True)

    key = models.CharField(max_length= 20, blank = True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return 'Email: {} key: {} created on: {}'.format(self.email, self.key, str(self.created_on))

"""
	CustomEmail Class

	Send a custom email to everyone in the subscription class
"""
class CustomEmail(models.Model):
	
	subject = models.CharField(max_length=255)

	"""
	TODO: 
	custom_recipients = models.CharField(max_length = 3000, 	
		null = True, 
		blank = True, 
		help_text = "Leave blank if you want to send to everyone in 'Subscriptions'. Seperate with comma")
	"""

	body = RichTextUploadingField()
	
	send_now = models.BooleanField(default = True, 
		help_text = "If this box is checked, the email will be sent directly after you press 'save'") 

	date_sent = models.DateTimeField(null = True, blank = True)

	""" 
		send custom email()
	"""
	def send_custom_email(self):
		if not self.send_now:
			return False

		context = {}
		context["body"] = self.body

		# Prevent the circle!!!!! 
		from subscriptions.utils import mass_mail_thread_helper

		"""
		TODO: 
		if self.custom_recipients:

			print("Sending to custom recipient(s): {}".format(self.custom_recipients))
			parsed_recipients = [x.strip() for x in self.custom_recipients.split(',')]
			recipient_tuples = []

			for recipient in parsed_recipients:
				subscription

			try:
				thread.start_new_thread( mass_mail_thread_helper,  
					('email_custom.html', self.subject,  context, parsed_recipients) )
			except Exception as e:
				print(str(e))
				return False

		# If recipients is none
		else:
		"""
		try:
			thread.start_new_thread(mass_mail_thread_helper, ('email_custom.html', self.subject, context))
		except Exception as e:
			print(str(e))
			return False

		self.date_sent = timezone.now()
		# All is good!
		return True
	
	def __str__(self):
		return 'Subject: {}, Sent On: {}'.format(self.subject, str(self.date_sent))

	
	def save(self):
		if self.save:
			self.send_custom_email()
		super(CustomEmail, self).save()
