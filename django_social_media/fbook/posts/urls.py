from django.urls import path 
from posts import views 
from .views import PostUpdateView,PostDeleteView
app_name='posts'
urlpatterns=[
	path('',views.list_post,name='my-post-view'),
	path('liked/',views.like_unlike,name='like-view'),
	path('<pk>/delete',PostDeleteView.as_view(),name='post-delete'),
	path('<pk>/update',PostUpdateView.as_view(),name='post-update'),
]