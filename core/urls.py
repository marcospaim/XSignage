from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("upload-media", views.upload_media, name="upload_media"),
    path("delete-media/<int:media_id>/", views.delete_media, name="delete_media"),
    path("playlists", views.playlists, name="playlists"),
    # path('playlist/create/', views.playlist_create, name='playlist_create'),
    path("playlist/list/", views.playlist_list, name="playlist_list"),
    path("get_subgroups/", views.get_subgroups, name="get_subgroups"),
    path("playlist/edit/<int:playlist_id>", views.edit_playlist, name="edit_playlist"),
    path("add-content/<int:playlist_id>/", views.add_content, name="add_content"),
    path("displays", views.displays, name="displays"),
    path('displays/<int:display_id>/edit/', views.edit_display, name='edit_display'),
    path("group/create/", views.group_create, name="group_create"),
    path("subgroup/create/", views.subgroup_create, name="subgroup_create"),
    path("group/list/", views.group_list, name="group_list"),
    path("groups", views.groups, name="groups"),
    path(
        "delete-content/<int:content_id>/", views.delete_content, name="delete_content"
    ),
    path(
        "display-browser/<int:playlist_id>/",
        views.display_browser,
        name="display_browser",
    ),
    path(
        "get-video-duration/<int:mediafile_id>/",
        views.get_video_duration,
        name="get_video_duration",
    ),
    path('display/', views.display_view, name='display-view'),
    path('display/<uuid:guid>/playlist/', views.get_display_playlist, name='get_display_playlist'),
]
# Debugging: Print URL patterns
for pattern in urlpatterns:
    print(pattern.pattern, pattern.name)
