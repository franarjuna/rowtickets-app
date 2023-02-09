from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from countries.viewsets import CountryViewSet
from events.viewsets import CategoryViewSet, EventViewSet
from faqs.viewsets import FAQViewSet
from tncs.viewsets import TnCViewSet

# Sentry debug function
def trigger_error(request):
    raise Exception('Debugging Sentry installation')

# Django Rest Framework setup
router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='countries')

countries_router = NestedSimpleRouter(router, r'countries', lookup='country')
countries_router.register(r'categories', CategoryViewSet)
countries_router.register(r'events', EventViewSet)
countries_router.register(r'faqs', FAQViewSet)
countries_router.register(r'tncs', TnCViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('sentry-debug-2d4795b5a4b00eb38d1a1db9a90ffd8c/', trigger_error),
    path(r'', include(router.urls)),
    path(r'', include(countries_router.urls))
]


if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
