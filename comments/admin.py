from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	# TODO: Filter by parent object
	# Problem: Find which parent object comment belongs to
    list_display = ('user', 'created_on')
    list_filter = ('created_on','user')