from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, Answer, UserProfile
from django.views.decorators.csrf import csrf_exempt
import json

def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if UserProfile.objects.filter(name=name).exists():
            return render(request, 'register.html', {'error': 'اسم قبلاً ثبت شده! اسم دیگه‌ای انتخاب کن.'})
        user = UserProfile.objects.create(name=name)
        request.session['user_id'] = user.id
        return redirect('quiz:quiz_home')
    return render(request, 'register.html')

def logout_user(request):
    request.session.flush()  # حذف همه داده‌های سشن (خروج کاربر)
    return redirect('quiz:register_user')  # هدایت به صفحه ثبت‌نام


def quiz_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('quiz:register_user')

    user = get_object_or_404(UserProfile, id=user_id)
    answered_questions = json.loads(user.answered_questions)

    questions = Question.objects.prefetch_related('answers').all()
    return render(request, 'quiz.html', {
        'questions': questions,
        'user': user,
        'answered_questions': answered_questions
    })



@csrf_exempt
def submit_answer(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'لطفاً ابتدا وارد شوید.'}, status=403)

        user = get_object_or_404(UserProfile, id=user_id)
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')

        answered = json.loads(user.answered_questions)

        if question_id in answered:
            return JsonResponse({'error': 'شما قبلاً به این سوال پاسخ داده‌اید!'}, status=400)

        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id, question=question)

        correct = answer.is_correct

        if correct:
            user.score += 1

        user.add_answered_question(question_id)

        return JsonResponse({'correct': correct, 'score': user.score})


def leaderboard(request):
    users = UserProfile.objects.order_by('-score')
    user_id = request.session.get('user_id')
    current_user = None
    if user_id:
        try:
            current_user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            request.session.flush()
            return redirect('quiz:register_user')
    return render(request, 'leaderboard.html', {'users': users, 'current_user': current_user})

def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('quiz:manage_users')
    return render(request, 'delete_confirm.html', {'user': user})

def manage_users(request):
    users = UserProfile.objects.all()
    return render(request, 'manage_users.html', {'users': users})