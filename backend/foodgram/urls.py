from rest_framework import routers
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static


from rest_framework.authtoken import views
from users.views import APISubscribe, APISubscriptions
from recipe.views import RecipeViewSet, ListIngredientsAPIView, RetrieveIngredientsAPIView, APIFavorites

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ingredients/', ListIngredientsAPIView.as_view()),
    path('api/ingredients/<int:pk>', RetrieveIngredientsAPIView.as_view()),
    path('api/recipes/<int:pk>/favorite/', APIFavorites.as_view()),
            
    path('api/users/subscriptions/', APISubscriptions.as_view()), 
    path('admin/', admin.site.urls),
    # path('api/auth/token/login/', views.obtain_auth_token),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    # url(r'^auth/', include('djoser.urls')),
    # url(r'^auth/', include('djoser.urls.authtoken')),
    path('api/users/<int:pk>/subscribe/', APISubscribe.as_view()),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Foodgram API",
      default_version='v1',
      description="Документация проекта Foodgram",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@foodgram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', 
       schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), 
       name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), 
       name='schema-redoc'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)