from django.template import Library

register = Library()

@register.filter
def has_ingredients(value):
	return len(value.all()) > 0
