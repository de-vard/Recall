from django.contrib import admin
from .models import CardProgress, StudySession
from flashcards.models import FlashCardSet, Card
from django.contrib.auth import get_user_model

User = get_user_model()


# ---------------- CARD PROGRESS ADMIN ---------------- #

@admin.register(CardProgress)
class CardProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "card", "is_known", "date_answer")
    search_fields = ("user__username", "user__email", "card__term", "card__definition")
    list_filter = ("is_known", "date_answer")
    autocomplete_fields = ("user", "card")
    ordering = ("-date_answer",)

    readonly_fields = ("date_answer",)
    fields = ("user", "card", "is_known", "date_answer")


# ---------------- STUDY SESSION ADMIN ---------------- #

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ("user", "flashcard_set", "start_time", "end_time", "cards_studied", "cards_known")
    search_fields = ("user__username", "user__email", "flashcard_set__title")
    list_filter = ("start_time", "end_time", "flashcard_set")
    autocomplete_fields = ("user", "flashcard_set")
    ordering = ("-start_time",)

    readonly_fields = ("start_time", "end_time")
    fields = (
        "user",
        "flashcard_set",
        "start_time",
        "end_time",
        "cards_studied",
        "cards_known",
    )
