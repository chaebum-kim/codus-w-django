from django.db import models
from django.conf import settings
from django.urls import reverse


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

    def tag_set_as_string(self):
        result = ''
        for tag in self.tag_set.all():
            result = result + '#' + tag.name + ' '
        return result

    def __str__(self):
        return f'Article #{self.id}'

    def get_absolute_url(self):
        return reverse('board:article_detail', args=[self.pk])

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
