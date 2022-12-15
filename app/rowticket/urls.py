from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# Sentry debug function
def trigger_error(request):
    raise Exception('Debugging Sentry installation')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('sentry-debug-8f0fae1a5f/', trigger_error),
]

# if settings.DEBUG:
#     # Swagger
#     SchemaView = get_schema_view(
#         openapi.Info(
#             title="Relevant API",
#             default_version='v1',
#             description="Endpoints disponibles en la API de Relevant",
#         ),
#         public=True,
#         permission_classes=(permissions.AllowAny,),
#         url=settings.SWAGGER_URL,
#     )
# 
#     urlpatterns.append(path('', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
