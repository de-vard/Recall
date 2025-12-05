from django.urls import path

from folders.views import FolderAPIRetrieve, FolderAPICreate, FolderRootView, FolderAPIUpdate

urlpatterns = [
    path("", FolderRootView.as_view(), name="folder-root"),
    path('<uuid:public_id>/', FolderAPIRetrieve.as_view(), name='folder-home'),
    path("create/<uuid:public_id>/", FolderAPICreate.as_view(), name='folder-create'),
    path("update/<uuid:public_id>/", FolderAPIUpdate.as_view(), name="folder-update"),
]
