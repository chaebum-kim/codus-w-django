from django.contrib import admin
from .models import Article, Comment, Scrap


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Scrap)
class ScrapAdmin(admin.ModelAdmin):
    pass
