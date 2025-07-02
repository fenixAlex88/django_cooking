from django.shortcuts import render, redirect
from .models import Post
from django.db.models import F
from .forms import PostAddForm, LoginForm, RegistrationForm
from django.contrib.auth import login, logout
from django.contrib import messages

def index(request):
	"""Для главной страницы"""
	posts = Post.objects.all()
	context = {
		'title': 'Главная страница',
		'posts': posts,
	}
	return render(request, 'cooking/index.html', context)

def category_list(request, pk):
	"""Реакция на нажатие кнопки категории"""
	posts = Post.objects.filter(category_id=pk)
	context = {
		'title': posts[0].category,
		'posts': posts,
	}
	return render(request, 'cooking/index.html', context)

def post_detail(request, pk):
	"""Страница статьи"""
	article = Post.objects.get(pk=pk)
	Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
	ext_posts = Post.objects.exclude(pk=pk).order_by('-watched')[:4]
	context = {
		'title': article.title,
		'post': article,
		'ext_posts': ext_posts,
	}
	return render(request, 'cooking/article_detail.html', context)

def add_post(request):
	"""Добавление статьи от пользователя, без админки"""
	if request.method == 'POST':
		form = PostAddForm(request.POST, request.FILES)
		if form.is_valid():
			post = Post.objects.create(**form.cleaned_data)
			post.save()
			messages.success(request, 'Статья успешно добавлена')
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostAddForm()

	context = {
		'title': 'Добавить статью',
		'form': form,
	}
	return render(request,'cooking/article_add_form.html',context)

def user_login(request):
	"""Аунтификация пользователя"""
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.success(request, 'Вы успешно вошли в аккаунт')
			return redirect('index')
	else:
		form = LoginForm()
	
	context = {
		'title': 'Авторизация пользователя',
		'form': form
	}
	return render(request, 'cooking/login_form.html', context)

def user_logout(request):
	"""Выход пользователя"""
	logout(request)
	messages.info(request, 'Вы вышли из аккаунта')
	return redirect('index')

def user_register(request):
	"""Регистрация пользователя"""
	if request.method == 'POST':
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Вы успешно зарегистрировали аккаунт')
			return redirect('login')
	else:
		form = RegistrationForm()
	context = {
		'title': 'Регистрация пользователя',
		'form': form,
	}
	return render(request, 'cooking/register_form.html', context)