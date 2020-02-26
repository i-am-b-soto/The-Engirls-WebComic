from django.contrib import admin

# Register your models here.
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_filter = ('category', 'created_on')
	list_display = ('title', 'created_on', 'category')
	search_fields = ('title',)
	#autocomplete_fields['tag__tag']
	

@admin.register(Comment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'Post', 'created_on')
    list_filter = ('created_on','name')



