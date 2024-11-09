from django.shortcuts import render
from .models import Post, Type
from . import functions
from .constants import Constants

def get_common_context():
    return {
        'types': Type.objects.all(),
        'title': Constants.SITE_NAME,
        'logo': Constants.SITE_LOGO,
        'flags': {'ru': 'Russia', 'en': 'United-Kingdom', 'fr': 'France', 'de': 'Germany', 'es': 'Spain', 'it': 'Italy', 'pt': 'Portugal', 'iw': 'Israel'},
        'disable_sidebar': False
    }

def get_posts_context():
    context = get_common_context()
    context['posts'] = Post.objects.all()
    return context

def home(request):
    context = get_posts_context()
    context['disable_sidebar'] = True
    return render(request, 'blog/home.html', context)

def about(request):
    context = get_common_context()
    return render(request, 'blog/about.html', context)

def contact(request):
    context = get_common_context()
    return render(request, 'blog/contact.html', context)

def posts(request):
    context = get_common_context()
    post_type = request.GET.get('type')
    if post_type:
        context['posts'] = Post.objects.filter(type__id=post_type)
    else:
        context['posts'] = Post.objects.all()
    return render(request, 'blog/posts.html', context)

def post(request, post_id):
    context = get_common_context()
    context['post'] = Post.objects.get(id=post_id)
    return render(request, 'blog/post.html', context)