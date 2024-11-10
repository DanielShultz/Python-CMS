from django.shortcuts import render, redirect
from django.contrib import messages
from . import models, functions, constants, forms

def get_common_context():
    return {
        'types': models.Type.objects.all(),
        'title': constants.Constants.SITE_NAME,
        'logo': constants.Constants.SITE_LOGO,
        'description': constants.Constants.SITE_DESCRIPTION,
        'flags': {'ru': 'Russia', 'en': 'United-Kingdom', 'fr': 'France', 'de': 'Germany', 'es': 'Spain', 'it': 'Italy', 'pt': 'Portugal', 'iw': 'Israel'},
        'disable_sidebar': False
    }

def get_posts_context():
    context = get_common_context()
    context['posts'] = models.Post.objects.all()
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
    context['posts'] = models.Post.objects.all()
    post_type = request.GET.get('type')
    if post_type:
        context['posts'] = context['posts'].filter(type__id=post_type)
    return render(request, 'blog/posts.html', context)

def post(request, post_id):
    context = get_common_context()
    try:
        context['post'] = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        messages.error(request, 'Такой пост не существует')
        return redirect('blog:home')

    context['comments'] = models.Comment.objects.filter(post=context['post'])
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = context['post']
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog-post', post_id=post_id)
    else:
        comment_form = forms.CommentForm()
    context['comment_form'] = comment_form
    return render(request, 'blog/post.html', context)

def delete_comment(request, post_id, comment_id):
    try:
        comment = models.Comment.objects.get(id=comment_id)
        if comment.author == request.user:
            comment.delete()
            messages.success(request, 'Комментарий удален!')
            return redirect('blog-post', post_id=post_id)
        else:
            messages.error(request, 'Вы не можете удалить этот комментарий.')
            return redirect('blog-post', post_id=post_id)
    except models.Comment.DoesNotExist:
        messages.error(request, 'Такого комментария не существует.')
        return redirect('blog-post', post_id=post_id)