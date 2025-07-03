from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from cooking.views import SwaggerApiDoc

schema_view = get_schema_view(
    openapi.Info(
        title="Cooking API",
        default_version='v1',
        description="Документация по API кулинарии",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('swagger-ui/', SwaggerApiDoc.as_view(), name='swagger-ui'),
    # re_path(r'^swagger(?P<format>\.json|\.yaml$)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]