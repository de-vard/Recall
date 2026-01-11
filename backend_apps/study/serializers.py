from rest_framework import serializers

from backend_apps.flashcards.models import Card


class CardSerializer(serializers.ModelSerializer):
    # todo: дублирование кода, такой же код находится в  сериализаторе flashcards наименование CardListShortSerializer
    """Сериализатор неизученных карточек для метода GET"""
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


class CardProgressInputSerializer(serializers.Serializer):
    card_id = serializers.UUIDField()
    is_known = serializers.BooleanField()


class StudySessionResultSerializer(serializers.Serializer):
    results = CardProgressInputSerializer(many=True)


class StudySessionHistorySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    flashcard_set_id = serializers.UUIDField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField(allow_null=True)
    cards_studied = serializers.IntegerField()
    cards_known = serializers.IntegerField()


class CardProgressHistorySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    card_id = serializers.UUIDField()
    session_id = serializers.IntegerField()
    is_known = serializers.BooleanField()
    date_answer = serializers.DateTimeField()
