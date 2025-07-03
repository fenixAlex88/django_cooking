from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from .models import Post, Category, Comment
from .forms import PostAddForm, LoginForm, RegistrationForm, CommentForm


# def index(request):
# 	"""Для главной страницы"""
# 	posts = Post.objects.all()
# 	context = {
# 		'title': 'Главная страница',
# 		'posts': posts,
# 	}
# 	return render(request, 'cooking/index.html', context)

class Index(ListView):
	"""Для главной страницы"""
	model = Post
	def get_queryset(self):
		return Post.objects.filter(is_published=True)
	context_object_name = 'posts'
	template_name = 'cooking/index.html'
	extra_context = {'title': 'Главная страница',}


# def category_list(request, pk):
# 	"""Реакция на нажатие кнопки категории"""
# 	posts = Post.objects.filter(category_id=pk)
# 	context = {
# 		'title': posts[0].category,
# 		'posts': posts,
# 	}
# 	return render(request, 'cooking/index.html', context)

class ArticleByCategory(Index):
	"""Реакция на нажатие кнопки категории"""
	def get_queryset(self):
		"""Изменяем фильтр"""
		return Post.objects.filter(category_id=self.kwargs['pk'], is_published=True)

	def get_context_data(self, *, object_list=None, **kwargs):
		"""Для динамических данных"""
		context = super().get_context_data()
		cat = Category.objects.get(pk=self.kwargs['pk'])
		context['title'] = cat.title
		return context

# def post_detail(request, pk):
# 	"""Страница статьи"""
# 	article = Post.objects.get(pk=pk)
# 	Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
# 	ext_posts = Post.objects.exclude(pk=pk).order_by('-watched')[:4]
# 	context = {
# 		'title': article.title,
# 		'post': article,
# 		'ext_posts': ext_posts,
# 	}
# 	return render(request, 'cooking/article_detail.html', context)

class PostDetail(DetailView):
	"""Страница статьи"""
	template_name = 'cooking/article_detail.html'
	def get_queryset(self):
		return Post.objects.filter(pk=self.kwargs['pk'], is_published=True)
	def get_context_data(self, *, object_list=None, **kwargs):
		Post.objects.filter(pk=self.kwargs['pk']).update(watched=F('watched') + 1)
		post = Post.objects.get(pk=self.kwargs['pk'])
		context = super().get_context_data()
		context['title'] = post.title
		context['ext_posts'] = Post.objects.exclude(pk=self.kwargs['pk']).order_by('-watched')[:4]
		if self.request.user.is_authenticated:
			context['comment_form'] = CommentForm
		context['comments'] = Comment.objects.filter(post=post)
		return context



# def add_post(request):
# 	"""Добавление статьи от пользователя, без админки"""
# 	if request.method == 'POST':
# 		form = PostAddForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			post = Post.objects.create(**form.cleaned_data)
# 			post.save()
# 			messages.success(request, 'Статья успешно добавлена')
# 			return redirect('post_detail', pk=post.pk)
# 	else:
# 		form = PostAddForm()
#
# 	context = {
# 		'title': 'Добавить статью',
# 		'form': form,
# 	}
# 	return render(request,'cooking/article_add_form.html',context)

class AddPost(CreateView):
	"""Добавление статьи от пользователя, без админки"""
	form_class = PostAddForm
	template_name = 'cooking/article_add_form.html'
	extra_context = {'title': 'Добавить статью',}
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdate(UpdateView):
	"""Изменение статьи"""
	model = Post
	form_class = PostAddForm
	template_name = 'cooking/article_add_form.html'
	extra_context = {'title': 'Изменить статью', }

class PostDelete(DeleteView):
	"""Удаление статьи"""
	model = Post
	success_url = reverse_lazy('index')
	context_object_name = 'post'
	extra_context = {'title': 'Удалить статью', }

class SearchResult(Index):
	"""Поиск слова в заголовках и содержании статей"""
	def get_queryset(self):
		word = self.request.GET.get('q')
		return Post.objects.filter(
			Q(title__icontains=word) | Q(content__icontains=word)
		)

def add_comment(request, post_id):
	"""Добавление комментария"""
	form = CommentForm(request.POST)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.user = request.user
		comment.post = Post.objects.get(pk=post_id)
		comment.save()
		messages.success(request, "Ваш комментарий успешно добавлен")
	return redirect('post_detail', pk=post_id)

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

def profile(request, user_id):
	"""Страница пользователя"""
	user = User.objects.get(pk=user_id)
	posts = Post.objects.filter(author=user)
	context = {
		'user': user,
		'posts': posts,
		'title': "Страница пользователя"
	}
	return render(request, 'cooking/profile.html', context)