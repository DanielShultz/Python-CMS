from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('posts/<str:type_id>', views.posts, name='blog-posts'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:post_id>', views.post, name='blog-post'),
    path('post/<int:post_id>/like', views.like_post, name='like-post'),
    path('post/<int:post_id>/comment', views.add_comment, name='add-comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete', views.delete_comment, name='delete-comment'),
    path('post/<int:post_id>/rate', views.rate_post, name='rate-post'),
    path('contact/', views.contact, name='blog-contact'),

    path('posts_generate/',views.generate_posts, name='generate-posts'),
]