from django.urls import path

from courses.views import CourseListAPIView, CourseRetrieveAPIView, CourseRetrieveUpdateDestroyAPIView, \
    SubscribeCourseAPI, UnsubscribeCourseAPI, LikeCourseAPI, CourseCreateAPIView

urlpatterns = [
    path('<uuid:public_id>/like-dislike/', LikeCourseAPI.as_view(), name="course-like-dislike"),
    path("<uuid:public_id>/subscribe/", SubscribeCourseAPI.as_view(), name="course-subscribe"),
    path('<uuid:public_id>/unsubscribe/', UnsubscribeCourseAPI.as_view(), name="course-unsubscribe"),
    path('<uuid:public_id>/detail/', CourseRetrieveAPIView.as_view(), name='course-detail'),
    path('<uuid:public_id>/edit/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-edit'),
    path('<uuid:public_id>/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path("", CourseListAPIView.as_view(), name="course-list"),
]
