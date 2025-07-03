from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from .views import *
from .yasg import urlpatterns as api_doc_urls

urlpatterns = [
    # Web pages
    # path('', cache_page(60 * 15)(Index.as_view()), name='index'),
    path('', Index.as_view(), name='index'),
    path('category/<int:pk>/', ArticleByCategory.as_view(), name='category_list'),
    path('post/add/', AddPost.as_view(), name='add_post'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', SearchResult.as_view(), name='search'),
    path('password/', UserChangePassword.as_view(), name='change_password'),
	path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
	path('comments/<int:post_id>/', load_comments, name='load_comments'),

    # Auth
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/<int:user_id>/', profile, name='profile'),


    # API auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API resources
    path('api/v1/posts/', CookingPostsAPI.as_view(), name='cooking_posts_api'),
    path('api/v1/posts/<int:pk>/', CookingPostAPIDetails.as_view(), name='cooking_post_api_details'),
    path('api/v1/categories/', CookingCategoryAPI.as_view(), name='cooking_categories_api'),
    path('api/v1/categories/<int:pk>/', CookingCategoryAPIDetails.as_view(), name='cooking_category_api_details'),
]

urlpatterns += api_doc_urls
