from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("upload-media", views.upload_media, name="upload_media"),
    path("delete-media/<int:media_id>/", views.delete_media, name="delete_media"),
    path("playlists", views.playlists, name="playlists"),
    #path("playlist-edit"),
    path("displays", views.displays, name="displays"),
]
# Debugging: Print URL patterns
for pattern in urlpatterns:
    print(pattern.pattern, pattern.name)