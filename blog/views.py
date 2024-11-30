from django.shortcuts import render, redirect
from django.contrib import messages
from . import models, functions, constants, forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest

def get_common_context(request=None):
    context = {
        'types': models.Type.objects.all(),
        'title': constants.SITE_NAME,
        'logo': constants.SITE_LOGO,
        'color': constants.SITE_COLOR,
        'description': constants.SITE_DESCRIPTION,
        'enable_multilingual': constants.SITE_ENABLE_MULTILINGUAL,
        'flags': constants.SITE_LANGUAGES,
        'disable_sidebar': False
    }
    if request and request.COOKIES.get('language'):
        context['language'] = request.COOKIES['language']
    return context

def get_posts_context():
    context = get_common_context()
    context['posts'] = models.Post.objects.all()
    return context

def home(request):
    context = get_posts_context()
    context['disable_sidebar'] = True
    context['banners'] = models.Banner.objects.all()
    return render(request, 'blog/home.html', context)

def about(request):
    context = get_common_context()
    return render(request, 'blog/about.html', context)

def contact(request):
    context = get_common_context()
    return render(request, 'blog/contact.html', context)

def posts(request, type_id):
    context = get_common_context()
    try:
        context['type'] = models.Type.objects.get(id=type_id)
    except models.Type.DoesNotExist:
        messages.error(request, 'Такого типа не существует')
        return redirect('blog:home')
    context['posts'] = models.Post.objects.filter(type=context['type'])
    return render(request, 'blog/posts.html', context)

def post(request, post_id):
    context = get_common_context()
    try:
        context['post'] = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        messages.error(request, 'Такой пост не существует')
        return redirect('blog:home')

    context['comments'] = models.Comment.objects.filter(post=context['post'])

    comment_form = forms.CommentForm()
    context['comment_form'] = comment_form
    return render(request, 'blog/post.html', context)

def like_post(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        messages.error(request, 'Такого поста не существует')
        return redirect('blog:home')

    post.like(request.user)
    return redirect('blog-post', post_id=post_id)

def add_comment(request, post_id):
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = models.Post.objects.get(id=post_id)
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog-post', post_id=post_id)
    else:
        comment_form = forms.CommentForm()
    context = get_common_context()
    context['comment_form'] = comment_form

def delete_comment(request, post_id, comment_id):
    try:
        comment = models.Comment.objects.get(id=comment_id)
    except models.Comment.DoesNotExist:
        messages.error(request, 'Такого комментария не существует.')
        return redirect('blog-post', post_id=post_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('blog-post', post_id=post_id)
    else:
        messages.error(request, 'Вы не можете удалить этот комментарий.')
        return redirect('blog-post', post_id=post_id)