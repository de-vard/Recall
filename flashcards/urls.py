from django.urls import path

from flashcards.views import FlashCardDetailAPIView, FlashCardUpdateDestroyAPIView, FlashCardCreateAPIView, \
    CardUpdateDestroyAPIView, CardCreateAPIView

urlpatterns = [
    path('<uuid:public_id>/detail/', FlashCardDetailAPIView.as_view(), name='flash_card_set-detail'),
    path('<uuid:public_id>/edit/', FlashCardUpdateDestroyAPIView.as_view(), name='flash_card_set-edit'),
    path('create/', FlashCardCreateAPIView.as_view(), name='flash_card_set-edit'),
    path('card/<uuid:public_id>/edit/', CardUpdateDestroyAPIView.as_view(), name='card-edit'),
    path('card/create/', CardCreateAPIView.as_view(), name='card-edit'),
]
