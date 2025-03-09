from django.contrib import admin
from .models import Question, Answer, UserProfile

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4  # همیشه ۴ گزینه نشان دهد

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'id')  # ستون‌های نمایش داده‌شده
    search_fields = ('text',)  # امکان جستجو بر اساس متن سوال

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'id')
    search_fields = ('name',)
    actions = ['reset_user_answers']

    def reset_user_answers(self, request, queryset):
        queryset.update(score=0, answered_questions='[]')
        self.message_user(request, "پاسخ‌های کاربران ریست شد.")




admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)