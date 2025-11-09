from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count

from abstract.models import AbstractModel, AbstractManager, ProxyModel

User = get_user_model()


class CourseQuerySet(models.QuerySet):
    """Оптимизированный QuerySet для модели Course"""

    def with_related(self):
        """Загружает связанные данные (author, folder) одним запросом"""
        return self.select_related("author", "folder")

    def with_students(self):
        """Предзагружает студентов через промежуточную таблицу"""
        return self.prefetch_related("students")

    def with_likes_count(self):
        """Добавляет аннотацию с количеством лайков"""
        return self.annotate(likes_count=Count('likes'))

    def public(self):
        """Фильтрация публичных курсов"""
        return self.filter(is_public=True)


class CourseManager(AbstractManager):
    """Кастомный менеджер для модели Course"""

    def get_queryset(self):
        """Возвращает  кастомный QuerySet  класса CourseQuerySet"""
        return CourseQuerySet(self.model, using=self._db)

    def with_related(self):
        """ Возвращает курсы с заранее загруженными связанными данными:
            автором и папкой (select_related используется для оптимизации запросов).
        """
        return self.get_queryset().with_related()

    def with_students(self):
        """ Возвращает курсы с предзагруженными студентами, записанными на них.
            Использует prefetch_related для уменьшения количества запросов.
        """
        return self.get_queryset().with_students()

    def public(self):
        """Возвращает только публичные курсы (is_public=True)."""
        return self.get_queryset().public()

    def with_likes_count(self):
        """ Добавляет к каждому курсу аннотированное поле likes_count,
            показывающее количество лайков. Использует агрегирующую функцию Count.
        """
        return self.get_queryset().with_likes_count()


class Course(AbstractModel, ProxyModel):
    """ Модель курсов, данная модель перегружена связями
        Не обращаться напрямую к .students.all(), а использовать prefetch_related
    """
    description = models.TextField(verbose_name="Описание", blank=True, )
    is_public = models.BooleanField(verbose_name="Публичный курс", default=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='authored_courses'
    )
    students = models.ManyToManyField(
        User,
        through='CourseStudent',
        verbose_name='Записанные на курс студенты',
        related_name='+'
    )
    folder = models.ForeignKey(
        'folders.Folder',
        on_delete=models.PROTECT,
        verbose_name="Папка, в которой находится курс",
        related_name="courses"  # Для получения курсов которые находятся в папке
    )
    likes = models.ManyToManyField(
        User,
        through='CourseLike',  # через промежуточную модель
        related_name='liked_courses',
        verbose_name="Лайки курса",
        blank=True
    )
    objects = CourseManager()  # Указываем свою модель

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["-created"]


class CourseStudent(models.Model):
    """Промежуточная модель для регистрации пользователя на курс"""
    ROLE_CHOICES = (
        ("teacher", "Преподаватель"),
        ("student", "Студент"),
        ("admin", "Администратор"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student", verbose_name="Роль")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")

    class Meta:
        verbose_name = 'Участник курса'
        verbose_name_plural = 'Участники курсов'
        constraints = [
            models.UniqueConstraint(fields=["course", "user"], name="unique_course_user")
        ]  # Один пользователь может быть записан только один раз на курс

    def __str__(self):
        return f'{self.user} записался на курс: {self.course}'


class CourseLike(models.Model):
    """Промежуточная модель лайков для курсов"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Лайк курса"
        verbose_name_plural = "Лайки курсов"
        constraints = [
            models.UniqueConstraint(fields=["course", "user"], name="unique_course_like")
        ]

    def __str__(self):
        return f"{self.user} лайкнул {self.course}"
