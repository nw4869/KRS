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


@register.filter
def examination_disabled(examination):
    return 'disabled' if examination.finish_time is not None else ''


@register.filter
def choice_disabled(choice, examination):
    return examination_disabled(examination)


@register.filter
def choice_answer_class(choice, question):
    return 'text-danger' if question.answer == choice else ''
