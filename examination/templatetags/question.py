from django import template

register = template.Library()


@register.filter
def question_display(value, index):
    return '{}. {}'.format(index + 1, value)


@register.filter
def choice_display(value, index):
    return '{}. {}'.format(chr(ord('A') + index), value)


@register.filter
def choice_checked(choice_id, last_question_choices):
    return 'checked' if str(choice_id) in last_question_choices.values() else ''
