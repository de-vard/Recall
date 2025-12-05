from django.db.models import Count
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, CourseStudent, CourseLike
from courses.permissions import IsAuthor
from courses.serializers import CourseListSerializer, CourseRetrieveSerializer, CourseDetailSerializer, CourseCreate


class CourseListAPIView(generics.ListAPIView):
    """Список курсов"""
    queryset = Course.objects.public(). \
        select_related("author", "folder"). \
        annotate(
        likes_count=Count('likes', distinct=True),  # ставим distinct для ликвидации дублей
        students_count=Count('students', distinct=True)  # ставим distinct для ликвидации дублей
    )
    serializer_class = CourseListSerializer


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр курска детально"""
    lookup_field = "public_id"
    lookup_url_kwarg = 'public_id'  # Явно указываем параметр URL для swagger
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

    def get_serializer_class(self):
        """ get_serializer_class - позволяет менять сериализатор
            выбираем сериализатор в зависимости от того подписан пользователь или нет
        """
        user = self.request.user
        course = self.get_object()
        is_enrolled = CourseStudent.objects.filter(user=user, course=course).exists()

        if is_enrolled:
            return CourseDetailSerializer  # когда пользователь подписан
        return CourseRetrieveSerializer  # когда нет

    def get_queryset(self):
        """Для управления queryset"""
        queryset = Course.objects.public().annotate(
            likes_count=Count('likes', distinct=True),  # ставим distinct для ликвидации дублей
            students_count=Count('students', distinct=True)  # ставим distinct для ликвидации дублей
        ).select_related("author", "folder").prefetch_related("students", "likes", "lessons")
        return queryset


class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр/редактирование курса """
    lookup_field = "public_id"
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        """Для управления queryset"""
        queryset = Course.objects.public().annotate(
            likes_count=Count('likes', distinct=True),  # ставим distinct для ликвидации дублей
            students_count=Count('students', distinct=True)  # ставим distinct для ликвидации дублей
        ).select_related("author", "folder").prefetch_related("students", "likes", "lessons")
        return queryset


class SubscribeCourseAPI(APIView):
    """Подписка на курс"""
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, public_id):
        course = get_object_or_404(Course, public_id=public_id)
        user = request.user
        if CourseStudent.objects.filter(user=user, course=course).exists():
            return Response({"detail": "Вы уже подписаны."}, status=400)
        else:
            CourseStudent.objects.create(user=user, course=course)
        return Response({"detail": "Успешно подписано!"}, status=201)


class UnsubscribeCourseAPI(APIView):
    """Отписка на курс"""
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, public_id):
        course = get_object_or_404(Course, public_id=public_id)
        user = request.user
        subscribe = CourseStudent.objects.filter(user=user, course=course).first()

        if not subscribe:
            return Response({"detail": "Вы не подписаны."}, status=400)
        else:
            subscribe.delete()
        return Response({"detail": "Успешно отписано!"}, status=200)


class LikeCourseAPI(APIView):
    """Лайк/дизлайк  курсу"""
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    def post(self, request, public_id):
        course = get_object_or_404(Course, public_id=public_id)
        user = request.user

        if CourseLike.objects.filter(user=user, course=course).exists():
            obj = CourseLike.objects.get(user=user, course=course)
            obj.delete()
            return Response({"detail": "Курс диздайкнут"}, status=200)
        else:
            CourseLike.objects.create(user=user, course=course)
            return Response({"detail": "Курс лайкнут"}, status=200)


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreate
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Подставляем автора и папку из URL
        folder_id = self.kwargs.get("public_id")  # это public_id папки
        serializer.save(author=self.request.user, folder_id=folder_id)
        # TODO: добавить проверку что бы наименования не повторялись как в папке
