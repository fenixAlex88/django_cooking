from django.urls import path

from .views import category_list, index, post_detail, add_post

urlpatterns = [
    path('', index, name='index'),
	path('category/<int:pk>/', category_list, name='category_list'),
	path('post/add', add_post, name='add_post'),
   	path('post/<int:pk>', post_detail, name='post_detail'),
]
