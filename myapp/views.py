from .utils import *
from django.shortcuts import  redirect, render
from .form import  UserForm ,UpdateProfile
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import *

def main(request):
    print(Question.objects.all().count())
    if Question.objects.all().count()<=5:
        generate_questions_with_answers(5)
    questions = Question.objects.all()
    return render(request, "home.html", {'questions': questions})

"""SignUp Form (Create User)"""
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, ("Registration Successful!"))
            return redirect('login_view')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {
        "form": form
    }
    
    return render(request, "login.html", context)

"""LogOut Page"""
def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect("login_view")

def update_profile(request):
    args = {}
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UpdateProfile(instance=request.user)

    args['form'] = form
    return render(request, 'update_profile.html', args)

"""Quiz Scorecard Page"""
def submit_quiz(request):
    questions = Question.objects.all()
    total_marks = 0
    correct_answers = 0
    incorrect_answers = 0

    for question in questions:
        selected_answers = request.POST.getlist(str(question.id))
        correct_answer_ids = set(
            Answer.objects.filter(
                question=question, is_correct=True
            ).values_list("id", flat=True)
        )
        selected_correct_answer_ids = set(map(int, selected_answers)) & correct_answer_ids

        if len(selected_correct_answer_ids) == len(correct_answer_ids):
            total_marks += question.marks
            correct_answers += 1
        else:
            incorrect_answers += 1

        Results.objects.create(
            user=request.user,
            total_marks=total_marks,
            correct_answers=correct_answers,
            incorrect_answers=incorrect_answers,
        )

    return render(
        request,
        "scorecard.html",
        {
            "total_marks": total_marks,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
        },
    )
