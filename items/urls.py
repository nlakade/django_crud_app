from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('weather/', views.WeatherAPIView.as_view(), name='weather-api'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('browse/', views.items_list_view, name='items-list'),
]