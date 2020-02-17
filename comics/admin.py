from django.contrib import admin

# Register your models here.
from .models import ComicPanel, Comment

"""
Deprecated
class tagInline(admin.StackedInline):
  model = Tag
  extra = 1
  search_fields = ['tag']
  #autocomplete_fields['tag']
"""

@admin.register(ComicPanel)
class ComicPanelAdmin(admin.ModelAdmin):

	exclude = ('thumbnail',)
	#inlines = [tagInline]
	list_filter = ('chapter', 'series')
	#search_fields = ['title','series','chapter']
	list_display = ('title','series', 'chapter', 'episode')
	#autocomplete_fields['tag__tag']
	

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'ComicPanel', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'body')



