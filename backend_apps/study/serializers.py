from rest_framework import serializers

from backend_apps.flashcards.models import Card


class CardSerializer(serializers.ModelSerializer):
    """Сериализатор неизученных карточек для метода GET"""

    class Meta:
        model = Card
        fields = ['public_id', 'term', 'definition']


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
