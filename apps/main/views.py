from django.shortcuts import render, redirect
from .models import Article, Comment, Like, Dislike, Category, ArticleViewsCount
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm
from django.views import generic

# reverse('contacts-page') -> /contacts/

# .get, .all, .filter, .create, .get_or_create

# ?key=value - query param - параметр GET запроса

# model_confirm_delete.html


class ArticleDeleteView(generic.DeleteView):
    model = Article
    template_name = 'main/article_confirm_delete.html'
    success_url = '/'
    pk_url_kwarg = 'article_id'



class ArticleUpdateView(generic.UpdateView):
    template_name = 'main/article_form.html'  # путь до html файла страницы
    model = Article  # указываем модель, данные которой будут обновляться
    form_class = ArticleForm  # форма для обновления данных из таблицы
    pk_url_kwarg = 'article_id'
    # success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        page_title = 'Изменить'
        context['page_title'] = page_title
        return context



def show_home_page(request):
    from django.urls import reverse

    query_params = request.GET

    articles = Article.objects.filter(is_active=True)

    if 'category_id' in query_params:
        category_id = query_params.get('category_id')

        # category__id - обращение к полю id в таблице Category
        articles = articles.filter(category__id=category_id)

    # [[1, [1,2,3]], [2, [1,2,3]], [3, [1]]]
    paginator = Paginator(articles, 3)
    page = request.GET.get('page')

    articles = paginator.get_page(page)

    context = {
        'articles': articles
    }

    return render(request, "main/index.html", context)


def show_category_articles_page(request, category_id):
    sort = request.GET.get('sort')

    if category_id == 'all':
        category = 'Все категории'
        articles = Article.objects.all().order_by(sort if sort else 'id')
    else:
        category = Category.objects.get(id=category_id)
        articles = Article.objects.filter(category=category).order_by(sort if sort else 'id')

    sort_fields = {
        'По названию': ['title', '-title'],
        'По просмотрам': ['views', '-views'],
        'По дате': ['created_at', '-created_at']
    }

    context = {
        'articles': articles,
        'category': category,
        'sort_fields': sort_fields
    }
    return render(request, 'main/category_articles.html', context)

# создать ссылку в urls
# данную ссылку вызвать в кнопках категорий




def show_contacts_page(request):
    return render(request, "main/contacts.html")

# templatetags
# сделать отображение Вопросов-ответов на главной странице


def show_article_page(request, article_id):
    # .get() - фильтрация по уникальному значению
    article = Article.objects.get(id=article_id)

    comments = Comment.objects.filter(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('article-page', article.id)
    else:
        form = CommentForm()

    # article.likes
    # article.dislikes

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    # objects.get_or_create()
    viewed_article, created = ArticleViewsCount.objects.get_or_create(article=article, user=request.user)
    if created:
        article.views += 1
        article.save()

    context = {
        'article': article,
        'form': form,
        'comments': comments
    }
    return render(request, 'main/article_page.html', context)


def show_faq_page(request):
    return render(request, 'main/faqs.html')


@login_required(login_url='users:login-user')  # http://127.0.0.1:8000/accounts/login/
def create_article_page(request):
    page_title = 'Создать' if 'create' in request.path else 'Изменить'

    if request.method == 'POST':
        # request.POST - словарь с текстовым контентом
        # request.FILES - словарь с файлами
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user  # AnonymousUser, User
            form.save()
            return redirect('article-page', form.id)
    else:
        form = ArticleForm()

    context = {
        'page_title': page_title,
        'form': form
    }
    return render(request, 'main/article_form.html', context)

# add_like
# add_dislike


def add_like_or_dislike(request, article_id, action):
    article = Article.objects.get(pk=article_id)

    if action == 'add_like':
        if request.user in article.likes.user.all():
            article.likes.user.remove(request.user.id)
        else:
            article.likes.user.add(request.user.id)
            article.dislikes.user.remove(request.user.id)
    elif action == 'add_dislike':
        if request.user in article.dislikes.user.all():
            article.dislikes.user.remove(request.user.id)
        else:
            article.dislikes.user.add(request.user.id)
            article.likes.user.remove(request.user.id)

    return redirect('article-page', article.id)



def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    article_id = comment.article.id

    comment.delete()
    return redirect('article-page', article_id)


def search(request):
    query = request.GET.get('q')
    if not query:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(title__iregex=query)

    total_likes = sum([article.likes.user.all().count() for article in articles])
    total_dislikes = sum([article.dislikes.user.all().count() for article in articles])
    total_views = sum([article.views for article in articles])
    total_comments = sum([article.comment_set.all().count() for article in articles])

    context = {
        'articles': articles,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_views': total_views,
        'total_comments': total_comments
    }
    return render(request, 'main/search.html', context)