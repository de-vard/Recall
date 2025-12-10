from rest_framework import serializers

from courses.models import Course
from flashcards.models import FlashCardSet, Card


class CardListShortSerializer(serializers.ModelSerializer):
    """Список карточек в модуле"""

    class Meta:
        model = Card
        fields = ('public_id', 'term', 'definition', 'transcription', 'image', 'sound')


class CourseShortSerializer(serializers.ModelSerializer):
    """Курс в котором находиться модуль"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('url', 'title')
        ref_name = 'FlashcardCourseShort'  # Другое уникальное имя

    def get_url(self, obj):
        return obj.get_absolute_url()


class FlashCardDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр урока/модуля"""

    cards = CardListShortSerializer(many=True, read_only=True)
    course = CourseShortSerializer(read_only=True)

    class Meta:
        model = FlashCardSet
        fields = ("title", "course", "cards")


class FlashCardCreateSerializer(serializers.ModelSerializer):
    """Детальный просмотр урока/модуля"""

    class Meta:
        model = FlashCardSet
        fields = "__all__"


class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["term", "definition", "transcription", "flashcard", "image", "sound"]
