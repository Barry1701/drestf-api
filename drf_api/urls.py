from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route

urlpatterns = [
    # Główna strona
    path('', root_route),
    
    # Panel administracyjny Django
    path('admin/', admin.site.urls),
    
    # Autoryzacja API
    path('api-auth/', include('rest_framework.urls')),
    
    # Ścieżki logout oraz auth dla `dj-rest-auth`
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # Prefiksy dla poszczególnych modułów
    path('api/profiles/', include('profiles.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/likes/', include('likes.urls')),
    path('api/followers/', include('followers.urls')),
    path('api/products/', include('products.urls')),
]
