from django import template

register = template.Library()


@register.filter
def question_display(value, index):
    return '{}. {}'.format(index + 1, value)


@register.filter
def choice_display(value, index):
    return '{}. {}'.format(chr(ord('A') + index), value)