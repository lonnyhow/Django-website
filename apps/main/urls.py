from django.urls import path

from . import views

# http://127.0.0.1:5000/
urlpatterns = [
    path('', views.show_home_page, name='home-page'),
    path('contacts/', views.show_contacts_page, name='contacts-page'),
    path('faqs/', views.show_faq_page, name='faq-page'),
    path('articles/<str:article_id>/', views.show_article_page, name='article-page'),
    path('articles/<str:article_id>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<str:article_id>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('create/', views.create_article_page, name='create-article'),
    path('articles/<str:article_id>/<str:action>/', views.add_like_or_dislike, name='vote'),
    path('categories/<str:category_id>/', views.show_category_articles_page, name='category-articles'),
    path('comments/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('search/', views.search, name='search')
]
