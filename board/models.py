from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag_set = models.ManyToManyField('Tag', blank=True)

    @property
    def count_comments(self):
        return self.comment_set.count()

    def tag_set_as_string(self):
        result = ''
        for tag in self.tag_set.all():
            result = result + '#' + tag.name + ' '
        return result

    def get_absolute_url(self):
        return reverse('board:article_detail', args=[self.pk])

    def __str__(self):
        return f'Article #{self.id}'

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)

    def serialize(self):
        return {
            'author': self.author.username,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': naturaltime(self.updated_at),
        }

    def __str__(self):
        return f'Comment #{self.id}'

    class Meta:
        ordering = ['id']


class Scrap(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    article_set = models.ManyToManyField(Article, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username
