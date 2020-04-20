from django.contrib import admin

# Register your models here.
from .models import Subscription, CustomEmail

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

	exclude = ('key',)
	list_filter = ('email',)
	

@admin.register(CustomEmail)
class CustomEmailAdmin(admin.ModelAdmin):
	readonly_fields = ['date_sent']
	list_filter = ['date_sent', 'subject']
	search_fields = ['date_sent']



