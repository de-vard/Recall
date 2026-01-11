from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_apps.flashcards.models import Card
from backend_apps.study.serializers import CardSerializer, StudySessionResultSerializer, CardProgressHistorySerializer, \
    StudySessionHistorySerializer
from backend_apps.study.services import StudyService, mongo
from backend_apps.study.utils import mongo_to_json


class StudyAPIView(APIView):
    """API для изучения карточек пользователя"""
    permission_classes = [IsAuthenticated, ]  # Todo: Добавить проверку что пользователь подписан на курс

    @swagger_auto_schema(
        operation_description="Получает список неизученных карточек для пользователя и набора",
        responses={200: CardSerializer(many=True)}
    )
    def get(self, request, flashcard_set_id, *args, **kwargs):
        """
            GET /api/v1/study/<flashcard_set_id>/
            Возвращает список карточек, которые пользователь ещё не знает.
        """
        user_id = request.user.public_id
        session = StudyService(user_id, flashcard_set_id)
        cards = session.get_cards_when_is_unknown()

        serializer = CardSerializer(cards, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Сохраняет прогресс по карточкам пользователя",
        request_body=StudySessionResultSerializer,
        responses={200: openapi.Response("Статус сохранения", schema=openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def post(self, request, flashcard_set_id, *args, **kwargs):
        """
        POST /api/v1/study/<flashcard_set_id>/

        Пример тела запроса:
        {
            "results": [
                {"card_id": "uuid_карточки_1", "is_known": true},
                {"card_id": "uuid_карточки_2", "is_known": false}
            ]
        }
        """
        serializer = StudySessionResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.public_id
        session = StudyService(user_id, flashcard_set_id)

        # Собираем словарь Card -> is_known
        result_dict = {}
        for item in serializer.validated_data['results']:
            card = Card.objects.get(public_id=item['card_id'])
            result_dict[card] = item['is_known']

        session.save_result_cards(result_dict)
        session.save_result_session()

        return Response({"status": "saved"}, status=status.HTTP_200_OK)

    def delete(self, request, flashcard_set_id, *args, **kwargs):
        """Удаление сессии как в Postgres так и в MongoBD"""
        user_id = request.user.public_id
        session = StudyService(user_id, flashcard_set_id)
        session.delete_session()

        return Response(
            {"status": "deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class StudySessionHistoryAPIView(APIView):
    """
    История всех сессий обучения пользователя по набору
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="История сессий обучения по набору карточек",
        responses={200: StudySessionHistorySerializer(many=True)}
    )
    def get(self, request, flashcard_set_id):
        user_id = request.user.public_id

        docs = mongo.get_studysession_history(user_id, flashcard_set_id)

        data = [mongo_to_json(doc) for doc in docs]

        serializer = StudySessionHistorySerializer(instance=data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CardProgressHistoryAPIView(APIView):
    """
    История изучения конкретной карточки
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="История изучения карточки",
        responses={200: CardProgressHistorySerializer(many=True)}
    )
    def get(self, request, card_id):
        user_id = request.user.public_id

        docs = mongo.get_cardprogress_history(user_id, card_id)

        data = [mongo_to_json(doc) for doc in docs]

        serializer = CardProgressHistorySerializer(instance=data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
