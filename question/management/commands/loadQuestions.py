from django.core.management.base import BaseCommand, CommandError
from argparse import FileType
import re
from question.models import *


class QuestionsParser:
    pattern = r'\"\d+、(.*?)\n\s*?A\)\s+(.*?)\s*B\)\s+(.*?)\s*C\)\s+(.*?)\s*D\)\s+(.*?)\s+答案：(\w)\"'

    def parse(self, text):
        questions = []
        raw_questions = re.findall(self.pattern, text, re.S)
        for question in raw_questions:
            question_content = question[0]
            choice_contents = question[1:-1]
            answer = question[-1]
            answer_index = ord(answer) - ord('A')
            questions.append({
                'question_content': question_content,
                'choice_contents': choice_contents,
                'answer_index': answer_index,
            })
        return questions


class Command(BaseCommand):
    help = 'Load questions from file'

    def add_arguments(self, parser):
        parser.add_argument('questions_files', nargs='+', type=FileType('r'))

    def handle(self, *args, **options):
        for question_file in options['questions_files']:
            with question_file as file:
                question_dicts = QuestionsParser().parse(file.read())
                questions = []
                for question_dict in question_dicts:
                    question = self.create_question(question_dict)
                    questions.append(question)
                self.create_question_set(questions)
                self.stdout.write(self.style.SUCCESS('successfully load questions count: {}'
                                                     .format(len(question_dicts))))

    def create_question(self, question):
        qs = ChoiceQuestion.objects.create(content=question['question_content'])
        for i in range(4):
            choice_content = question['choice_contents'][i]
            choice = Choice.objects.create(question=qs, content=choice_content)
            if i == question['answer_index']:
                qs.answer = choice
                qs.save()
        return qs

    def create_question_set(self, questions):
        question_set = QuestionSet.objects.create(name='unnamed', description='nothing')
        for question in questions:
            question_set.questions.add(question)
        question_set.save()
        return question_set