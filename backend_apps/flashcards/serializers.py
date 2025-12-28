from rest_framework import serializers

from backend_apps.courses.models import Course
from backend_apps.flashcards.models import FlashCardSet, Card


class CardListShortSerializer(serializers.ModelSerializer):
    """Список карточек в модуле"""
    image = serializers.SerializerMethodField()
    sound = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('public_id', 'term', 'definition', 'transcription', 'image', 'sound')

    def get_image(self, obj):
        if not obj.image or not obj.image.path_file:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.path_file.url)

    def get_sound(self, obj):
        if not obj.sound or not obj.sound.path_file:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.sound.path_file.url)


class CourseShortSerializer(serializers.ModelSerializer):
    """Курс в котором находиться модуль"""

    class Meta:
        model = Course
        fields = ('title', 'public_id')
        ref_name = 'FlashcardCourseShort'  # Другое уникальное имя


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
