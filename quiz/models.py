from django.db import models
import json

class Question(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='media/questions/', blank=True, null=True)

    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserProfile(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score = models.IntegerField(default=0)
    answered_questions = models.TextField(default='[]')  # لیست JSON سوال‌های جواب‌داده‌شده

    def __str__(self):
        return self.name

    def add_answered_question(self, question_id):
        answered = json.loads(self.answered_questions)
        if question_id not in answered:
            answered.append(question_id)
            self.answered_questions = json.dumps(answered)
            self.save()