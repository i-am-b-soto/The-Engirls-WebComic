from django.contrib import admin

# Register your models here.
from .models import Subscription

@admin.register(Subscription)
class ComicPanelAdmin(admin.ModelAdmin):

	#exclude = ('key',)
	#inlines = [tagInline]
	list_filter = ('email',)
	




