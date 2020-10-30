from django.urls import path 
from profiles import views
from profiles.views import ProfileListView,ProfileDetailView
app_name='profiles'
urlpatterns=[
	path('',views.ProfileListView.as_view(),name='all-profiles-view'),
	path('myprofile/',views.my_profile_view,name='my-profile-view'),
	path('invites/',views.invites_received_view,name='my-invites-view'),
	path('<slug>/',views.ProfileDetailView.as_view(),name='profile-detail-view'),
	path('to-invite/',views.inv_profile_list_view,name='invite-profile-view'),
	path('send-invite/',views.send_invatation,name='send-invite'),
	path('reject/',views.remove_from_friends,name='delete_invitation'),
	path('accept-invite/',views.invite_accept,name='invite_accept'),
	path('delete-invite/',views.invite_reject,name='invite_delete'),
]