from django.contrib import admin

# Register your models here.
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_filter = ('category', 'created_on')
	list_display = ('title', 'created_on', 'category')
	search_fields = ('title',)
	#autocomplete_fields['tag__tag']
	



