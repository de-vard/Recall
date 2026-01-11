from django.db.models import Count, Q
from rest_framework import viewsets, serializers, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend_apps.courses.models import Course, CourseStudent, CourseLike
from backend_apps.courses.permissions import IsSubscribe, IsAuthor
from backend_apps.courses.serializers import CourseDetailSerializer, CourseCreateSerializer, CourseListSerializer


class CourseViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    lookup_field = "public_id"
    lookup_url_kwarg = "public_id"
    _course_object = None  # для кеширования, экземпляр класса, который хранит уже загруженный объект курса.

    def get_object(self):
        """ get_object - это полный контроль над выборкой объекта.
            Используем для оптимизации запросов. Мы получаем объект сущности
            и помещаем в переменную _course_object, и если этот метод вызывают второй раз
            то возвращается уже вычисленный результат и не делается запрос в БД. Тем самым
            сокращаются запросы. Данный метод вызывается во многих других
            методов(get_serializer_class, get(),get_serializer() и так далее),
            так что при переопределении get_object необходимо всегда его оптимизировать.
        """
        if self._course_object is None:
            self._course_object = super().get_object()
        return self._course_object

    def get_queryset(self):
        """Возвращаем кверисеты в зависимости от метода"""
        if self.action == "list":
            return (
                Course.objects.public()
                .select_related("author", "folder")
                .annotate(
                    likes_count=Count("likes"), students_count=Count("students")
                ).order_by("-likes_count")
            )
        if self.action == "retrieve":
            return (
                Course.objects.all()
                .select_related("author", "folder")
                .prefetch_related("students", "likes", "lessons")
                .annotate(
                    likes_count=Count("likes", distinct=True),  # Добавляем поле количество лайков
                    students_count=Count("students", distinct=True),  # Добавляем поле количество студентов
                )
            )

        return Course.objects.all()

    def get_permissions(self):
        """Ограничение по методам"""
        # Словарь соответствия действий и разрешений
        permission_map = {
            'list': [IsAuthenticated],
            'create': [IsAuthenticated],
            'retrieve': [IsAuthenticated],  # автор ли или подписан он на курс
            'update': [IsAuthor],  # автор ли
            'partial_update': [IsAuthor],  # автор ли
            'destroy': [IsAuthor],  # автор ли
            'metadata': [IsAuthenticated],  # метаданные
            'subscribe_unsubscribe': [IsAuthenticated],
            'like_dislike': [IsAuthenticated],
        }

        # Получаем permission_classes для текущего действия или пустой список по умолчанию
        permission_classes = permission_map.get(self.action, [])

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Выбор сериализатора """

        if self.action == "retrieve":
            return CourseDetailSerializer
        if self.action == "create":
            return CourseCreateSerializer
        if self.action in ("update", "partial_update"):
            return CourseCreateSerializer

        return CourseListSerializer

    def perform_create(self, serializer):
        """Перед созданием курса"""
        validated_data = serializer.validated_data
        folder = validated_data.get('folder')

        if not folder:
            raise serializers.ValidationError({"folder": "Это поле обязательно для заполнения."})

        # Проверяем, что текущий пользователь является автором папки
        if folder.owner != self.request.user:
            raise serializers.ValidationError(
                {"folder": "Вы можете добавлять курсы только в свои собственные папки."}
            )

        serializer.save(author=self.request.user, folder=folder)

    @action(detail=True, methods=['post'], url_path='subscribe_unsubscribe')
    def subscribe_unsubscribe(self, request, public_id=None):
        """Подписка/отписка на курс"""
        course = self.get_object()
        user = request.user
        subscription, created = CourseStudent.objects.get_or_create(user=user, course=course)

        if created:
            message = "Успешно подписано!"
            http_status = status.HTTP_201_CREATED
            action_type = "subscribed"
        else:
            subscription.delete()
            message = "Успешно отписано!"
            http_status = status.HTTP_200_OK
            action_type = "unsubscribed"

        return Response({"detail": message, "action": action_type, }, status=http_status)

    @action(detail=True, methods=['post'], url_path='like_dislike')
    def like_dislike(self, request, public_id=None):
        """Лайк/дизлайк курса."""
        course = self.get_object()
        user = request.user

        like, created = CourseLike.objects.get_or_create(user=user, course=course)

        if created:
            message = "Курс лайкнут"
            action_type = "liked"
        else:
            like.delete()
            message = "Курс дизлайкнут"
            action_type = "disliked"

        return Response({"detail": message, "action": action_type, })

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        user = request.user

        queryset = (
            Course.objects.filter(Q(author=user) | Q(students=user))
            .select_related("author", "folder")
            .annotate(
                likes_count=Count("likes", distinct=True),
                students_count=Count("students", distinct=True),
            ).distinct()
        )

        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


