from django.urls import path

from . import views

urlpatterns = [
    path('', views.StartingPageView.as_view(), name='index-page'),
    path('posts', views.AllPostsView.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.PostDetailsView.as_view(), name='post-details-page'),
    path('read-later',views.ReadLaterView.as_view(),name='read-later-page')
]
