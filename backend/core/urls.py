from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chess.views import GameViewSet

# Cria as rotas automaticamente
router = DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]