from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User

# GET, POST, PUT, DELETE

def logout_user(request):
    logout(request)
    return redirect('users:login-user')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():  # проверяет правильность отправленных данных
            user = form.get_user()  # получает пользователя по username и password
            if user is not None:
                login(request, user)
                return redirect('home-page')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # происходит отправка данных в таблицу к привязанной модели
            return redirect('users:login-user')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)

# .get() - received more than 1 object


def show_author_profile(request, username):
    author = User.objects.get(username=username)
    author_articles = author.article_set.all()
    # получить общее количество комментариев всех статей пользователя

    total_likes, total_dislikes = 0, 0
    if author_articles:
        total_likes = sum([article.likes.user.all().count() for article in author_articles])
        total_dislikes = sum([article.dislikes.user.all().count() for article in author_articles])

    user_info = {
        'username': author.username,
        'email': author.email,
        'registered at': author.date_joined,
        'total articles': author_articles.count(),
        'total comments': sum([article.comment_set.all().count() for article in author_articles]),
        'total likes': total_likes,
        'total dislikes': total_dislikes,
        'total views': sum([article.views for article in author_articles])
    }

    # if request.user.is_authenticated:
    #     user_info

    context = {
        'author': author,
        'user_info': user_info
    }
    return render(request, 'users/profile.html', context)

