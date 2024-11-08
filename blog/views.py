from django.shortcuts import render
from .models import Post, Type
from .functions import get_range
from .constants import Constants

def get_common_context():
    return {
        'types': Type.objects.all(),
        'title': Constants.SITE_NAME,
        'logo': Constants.SITE_LOGO,
        'flags': {'ru': 'Russia', 'en': 'United-Kingdom', 'fr': 'France', 'de': 'Germany', 'es': 'Spain', 'it': 'Italy', 'pt': 'Portugal', 'iw': 'Israel'}
    }

def home(request):
    context = get_common_context()
    context['posts'] = Post.objects.all()
    return render(request, 'blog/home.html', context)


def about(request):
    context = get_common_context()
    return render(request, 'blog/about.html', context)

