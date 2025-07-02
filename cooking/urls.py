from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
	path('category/<int:pk>/', category_list, name='category_list'),
	path('post/add', add_post, name='add_post'),
   	path('post/<int:pk>', post_detail, name='post_detail'),
	path('login/', user_login, name='login'),
	path('logout/', user_logout, name='logout'),
	path('register/', user_register, name='register'),
]
