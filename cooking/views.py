from django.shortcuts import render
from .models import Post
from django.db.models import F

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
