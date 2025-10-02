from apps.main.models import Category, FAQ

from django.template import Library

register = Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.all()
    total_articles = 0
    for category in categories:
        category_articles_total = category.article_set.all().count()
        total_articles += category_articles_total
    return categories, total_articles


@register.simple_tag()
def get_faqs():
    return FAQ.objects.all()
