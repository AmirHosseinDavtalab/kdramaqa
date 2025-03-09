from django import template
from quiz.models import UserProfile

from django import template

register = template.Library()

@register.filter
def get_user_name(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        return user.name
    except UserProfile.DoesNotExist:
        return "ناشناس"

@register.filter
def get_score(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        return user.score
    except UserProfile.DoesNotExist:
        return 0

register = template.Library()

@register.filter
def get_score(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        return user.score
    except UserProfile.DoesNotExist:
        return 0

