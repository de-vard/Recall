from django.urls import path

from courses.views import CourseRetrieveAPIView

# TODO: Затычка убери курс и поставь уроки
urlpatterns = [
    path('<uuid:public_id>/detail/', CourseRetrieveAPIView.as_view(), name='flash_card_set-detail'),
]
