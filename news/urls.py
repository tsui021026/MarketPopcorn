from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', views.home, name='news-home'),
    path('daily/', PostListView.as_view(), name='news'),
    path('story/<slug:slug>-<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),
]