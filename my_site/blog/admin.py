from django.contrib import admin

from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "date", "tags")
    list_display = ("title", "author", "date")

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    list_filter = ("first_name", "last_name")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")
    list_filter = ("user_name",)

admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
