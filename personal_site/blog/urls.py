from django.urls import path
from django.contrib import admin
from . import views 

from django.conf import settings
from django.conf.urls.static import static
from blog.views import PhotoListView, PhotoCreateView, PhotoDetailView, PhotoDeleteView, PhotoVoteToggle, PhotoSaveView, PostDetail, PersonalListView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('gallery/', PhotoListView.as_view(), name='gallery'),
    path('personal/', PersonalListView.as_view(), name='personal-saves'),
    path('gallery/<str:order>/', PhotoListView.as_view(), name='gallery-param'),
    path('new_post/', PhotoCreateView.as_view(), name='new_post'),
    path('post2/<int:pk>/', PostDetailView.as_view(), name = 'post2-detail'),
    path('post2/<int:pk>/update/', PostUpdateView.as_view(), name = 'post2-update'),
    path('post2/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post2-delete'),
    path('post2/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<pk>/', PostDetail.as_view(), name='detail'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name = 'photo-detail'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name = 'photo-delete'),
    path('photos/<int:pk>/save/', PhotoSaveView.as_view(), name = 'photo-save'),
    path('photos/<int:pk>/motivate/', PhotoVoteToggle.as_view(), name = 'photo-vote')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
