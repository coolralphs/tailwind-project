from django import template

register = template.Library()

@register.filter
def alphabet_counter(value):
    return chr(ord('A') + value - 1)

@register.filter
def unique_by(queryset, field_name):
    seen = set()
    result = []
    for obj in queryset:
        field_value = getattr(obj, field_name)
        if field_value not in seen:
            seen.add(field_value)
            result.append(obj)
    return result

@register.filter
def dictsorttwo(value, key):
    return dict(sorted(value.items(), key=lambda item: item[key]))