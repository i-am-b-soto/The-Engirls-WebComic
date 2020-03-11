from django.contrib import admin

# Register your models here.
from .models import ComicPanel


@admin.register(ComicPanel)
class ComicPanelAdmin(admin.ModelAdmin):

	exclude = ('thumbnail',)
	#inlines = [tagInline]
	list_filter = ('chapter', 'series')
	#search_fields = ['title','series','chapter']
	list_display = ('title','series', 'chapter', 'page')
	#autocomplete_fields['tag__tag']
	




