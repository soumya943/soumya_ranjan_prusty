# generate_questions.py

import random
from faker import Faker
from django.contrib.auth.models import User
from myapp.models import Question, Answer

fake = Faker()

def generate_random_answers(num_answers, num_correct):
    all_answers = []
    for _ in range(num_answers):
        answer_text = fake.text(max_nb_chars=50)
        is_correct = True if num_correct > 0 else False
        all_answers.append({'answer_text': answer_text, 'is_correct': is_correct})
        num_correct -= 1
    return all_answers

def generate_questions_with_answers(num_questions):
    for _ in range(num_questions):
        question_text = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
        marks = 2
        num_answers = random.randint(5,5)
        num_correct = random.randint(1,2)
        answers = generate_random_answers(num_answers, num_correct)

        question = Question.objects.create(question_text=question_text, marks=marks)
        for answer_data in answers:
            Answer.objects.create(question=question, **answer_data)
