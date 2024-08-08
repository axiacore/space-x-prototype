from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.inclusion_tag('layout/_meta.html')
def meta_tags(title=None, description=None, image=None, page_type='website'):
    if not title:
        title = 'Business Strategy, Product Design, and Software Development'

    if not description:
        description = 'Axiacore is a digital studio specializing in business strategy, \
product design, and software development.'

    if not image:
        image = static('img/social-shared.jpg')

    if image.startswith('/'):
        image = f'{settings.BASE_URL}{image}'

    return {
        'title': title,
        'description': description,
        'image': image,
        'page_type': page_type,
    }
