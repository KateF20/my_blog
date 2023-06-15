from django.contrib import admin
from django.utils.text import Truncator

from .models import Author, Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'tags', 'date',)
    list_display = ('title', 'date', 'author',)
    prepopulated_fields = {'slug': ('title', )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'short_comment')

    def short_comment(self, comment):
        return Truncator(comment.text).chars(50)


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
