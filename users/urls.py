from django.urls import path

from users.views import UserAPIView, UserAPIRetrieve, MeAPIRetrieve, UnfollowUserAPI, FollowUserAPI

urlpatterns = [

    path("<uuid:public_id>/follow/", FollowUserAPI.as_view(), name="user-follow"),
    path('<uuid:public_id>/unfollow/', UnfollowUserAPI.as_view(), name="user-unfollow"),
    path('<uuid:public_id>/detail/', UserAPIRetrieve.as_view(), name='user-detail'),
    path('<uuid:public_id>/me-detail/', MeAPIRetrieve.as_view(), name='me-detail'),
    path('', UserAPIView.as_view(), name='user-list'),
]
