from django.shortcuts import render, redirect
from django.contrib import messages
from . import models, functions, constants, forms
from .templatetags import custom_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.db.models import Avg, Count

def get_common_context(request=None):
    context = {
        'types': models.Type.objects.all(),
        'title': constants.SITE_NAME,
        'logo': constants.SITE_LOGO,
        'color': constants.SITE_COLOR,
        'description': constants.SITE_DESCRIPTION,
        'enable_multilingual': constants.SITE_ENABLE_MULTILINGUAL,
        'flags': constants.SITE_LANGUAGES,
        'disable_sidebar': False,
        'private': constants.SITE_PRIVATE
    }
    if request and request.COOKIES.get('language'):
        context['language'] = request.COOKIES['language']
    return context

def get_posts_context():
    context = get_common_context()
    context['posts'] = models.Post.objects.all()
    context['types'] = models.Type.objects.prefetch_related('posts').all()  # Добавьте эту строку
    return context

def home(request):
    context = get_common_context()
    context['disable_sidebar'] = True
    context['banners'] = models.Banner.objects.filter(is_active=True)
    
    # Получаем посты с аннотацией среднего рейтинга, сортируем и ограничиваем
    posts_by_type = {}
    for type_obj in models.Type.objects.all():
        posts = models.Post.objects.filter(types=type_obj)\
            .annotate(avg_rating=Avg('ratings__value'))\
            .order_by('-avg_rating', '-date_posted')\
            .distinct()[:3]  # Берем 3 уникальных поста с самым высоким рейтингом
        
        if posts.exists():  # Добавляем только если есть посты
            posts_by_type[type_obj] = posts
    
    context['posts_by_type'] = posts_by_type
    return render(request, 'blog/home.html', context)

def about(request):
    context = get_common_context()
    return render(request, 'blog/about.html', context)

def contact(request):
    context = get_common_context()
    return render(request, 'blog/contact.html', context)

def posts(request, type_id):
    context = get_common_context()
    
    sort_by = request.GET.get('sort', '-avg_rating')
    
    valid_sorts = {
        '-date_posted': 'Новые сначала',
        'date_posted': 'Старые сначала',
        '-avg_rating': 'Высокий рейтинг',
        'avg_rating': 'Низкий рейтинг',
        '-likes_count': 'Популярные'
    }

    try:
        post_type = models.Type.objects.get(id=type_id)
    except models.Type.DoesNotExist:
        messages.error(request, 'Такого типа не существует')
        return redirect('blog-home')
    
    posts = models.Post.objects.filter(types=post_type)\
        .annotate(
            avg_rating=Avg('ratings__value'),
            likes_count=Count('likes')
        )
    
    if sort_by in valid_sorts:
        posts = posts.order_by(sort_by)
    
    context['sort_options'] = valid_sorts
    context['current_sort'] = sort_by
    context['type'] = post_type
    context['posts'] = posts
    
    return render(request, 'blog/posts.html', context)

def post(request, post_id):
    context = get_common_context()
    post_obj = get_object_or_404(models.Post, id=post_id)
    context['post'] = post_obj
    context['comments'] = post_obj.comments.filter(is_active=True)
    
    if request.user.is_authenticated:
        try:
            context['user_rating'] = post_obj.ratings.get(user=request.user).value
        except models.PostRating.DoesNotExist:
            context['user_rating'] = None
    
    context['comment_form'] = forms.CommentForm()
    return render(request, 'blog/post.html', context)

def generate_posts(request):
    post_type = models.Type.objects.first()
    if not post_type:
        messages.error(request, 'Тип поста не найден')
        return redirect('blog-home')

    posts = [
        models.Post(
            title=f'Заголовок поста {i}',
            content=f'Содержание поста {i}',
            type=post_type,
            author=request.user
        )
        for i in range(2000)
    ]
    models.Post.objects.bulk_create(posts)
    messages.success(request, 'Посты успешно созданы')
    return redirect('blog-home')

def like_post(request, post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        messages.error(request, 'Такого поста не существует')
        return redirect('blog-home')

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
    
@login_required
def rate_post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating', 0))
        rating_value = rating_value + 1
        
        if 1 <= rating_value <= 10:
            rating, created = models.PostRating.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'value': rating_value}
            )
            messages.success(request, 'Ваша оценка сохранена!')
        else:
            messages.error(request, 'Неверное значение оценки')
    
    return redirect('blog-post', post_id=post_id)