from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from backend_apps.media.models import Image, Sound
from .serializers import ImageSerializer, SoundSerializer


# TODO: код заглушка, пока не знаю как пользователь будет работать с медиа,
#  в дальнейшем нужно будет его изменить
class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by_user=self.request.user)


class SoundViewSet(ModelViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by_user=self.request.user)
