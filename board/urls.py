from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/new/', views.article_new, name='article_new'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:pk>/scrap/', views.article_scrap, name='article_scrap'),
    path('article/<int:pk>/unscrap/',
         views.article_unscrap, name='article_unscrap'),

    path('article/<int:article_pk>/comment/new/',
         views.comment_new, name='comment_new'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
