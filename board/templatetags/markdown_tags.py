from django import template
import markdown

register = template.Library()


@register.filter
def convert_markdown(content):
    return markdown.markdown(content, extensions=['extra', 'nl2br'])
