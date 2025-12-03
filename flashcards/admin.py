from django.contrib import admin
from .models import FlashCardSet, Card


# ---------------------- INLINE CARD ---------------------- #

class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    autocomplete_fields = ("image", "sound")
    fields = ("term", "definition", "transcription", "image", "sound", "created")
    readonly_fields = ("created",)
    show_change_link = True


# ---------------------- FLASHCARD SET ADMIN ---------------------- #

@admin.register(FlashCardSet)
class FlashCardSetAdmin(admin.ModelAdmin):
    list_display = ("public_id", "title", "course", "created", "updated")
    search_fields = ("title", "course__title")
    list_filter = ("course", "created")
    autocomplete_fields = ("course",)
    ordering = ("-created",)

    inlines = [CardInline]

    readonly_fields = ("created", "updated")
    fields = ("title", "course", ("created", "updated"))


# ---------------------- CARD ADMIN ---------------------- #

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("term", "flashcard", "created")
    search_fields = ("term", "definition", "flashcard__title")
    list_filter = ("flashcard", "created")
    autocomplete_fields = ("flashcard", "image", "sound")
    ordering = ("-created",)

    readonly_fields = ("created", "updated")
    fields = (
        "term",
        "definition",
        "transcription",
        "flashcard",
        "image",
        "sound",
        ("created", "updated"),
    )
