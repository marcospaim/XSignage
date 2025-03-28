from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
import json
import hashlib
import subprocess

from .forms import MediaFileForm, PlaylistForm, GroupForm, SubgroupForm
from .models import MediaFile, Playlist, Group, Subgroup, Content, CustomPage
from .serializers import serialize_contents

@login_required
def index(request):
    return render(request, "main.html")

@login_required
def upload_media(request):
    if request.method == "POST":
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            media_files = MediaFile.objects.all()
            context = {
                "media_files": media_files,
                "message": "File uploaded successfully!",
            }
            return render(request, "partials/mediafiles-list.html", context)
    media_files = MediaFile.objects.all()

    # Pass the queryset to the template context
    context = {"media_files": media_files}
    return render(request, "upload_media.html", context)

@login_required
def delete_media(request, media_id):
    if request.method == "DELETE":
        media_file = get_object_or_404(MediaFile, id=media_id)
        media_file.delete()
        media_files = MediaFile.objects.all()
        context = {"media_files": media_files, "message": "File deleted!"}
        return render(request, "partials/mediafiles-list.html", context)

@login_required
def playlists(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            # Redirect or return a success message
            return redirect("core:playlist_list")

    form = PlaylistForm()
    playlists = Playlist.objects.select_related("group", "subgroup").all()
    context = {
        "form": form,
        "playlists": playlists,
    }
    return render(request, "playlists.html", context)

@login_required
def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, "partials/playlist_list.html", {"playlists": playlists})

@login_required
def get_subgroups(request):
    group_id = request.GET.get("group_id")
    subgroups = Subgroup.objects.filter(group_id=group_id)
    # Include a default empty option
    subgroup_options = '<option value="">---------</option>' + "".join(
        [
            f'<option value="{subgroup.id}">{subgroup.name}</option>'
            for subgroup in subgroups
        ]
    )
    return HttpResponse(subgroup_options)

@login_required
def group_create(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:group_list")
    else:
        form = GroupForm()
    return render(request, "partials/group_form.html", {"form": form})

@login_required
def subgroup_create(request):
    if request.method == "POST":
        form = SubgroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:group_list")
    else:
        form = SubgroupForm()
    return render(request, "partials/subgroup_form.html", {"form": form})

@login_required
def group_list(request):
    groups = Group.objects.all()
    subgroupform = SubgroupForm()
    context = {
        "groups": groups,
        "subgroupform": subgroupform,
    }
    return render(request, "partials/group_list.html", context)

@login_required
def groups(request):
    groups = Group.objects.prefetch_related("subgroup_set").all()
    groupform = GroupForm()
    subgroupform = SubgroupForm()
    context = {
        "groupform": groupform,
        "subgroupform": subgroupform,
        "groups": groups,
    }
    return render(request, "groups.html", context)

@login_required
def edit_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    mediafiles = MediaFile.objects.all()
    custompages = CustomPage.objects.all()

    context = {
        "playlist": playlist,
        "mediafiles": mediafiles,
        "custompages": custompages,
    }
    return render(request, "edit_playlist.html", context)

@login_required
def add_content(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)

    if request.method == "POST":
        mediafile_id = request.POST.get("mediafile")
        custompage_id = request.POST.get("custompage")
        duration = request.POST.get("duration")

        if mediafile_id:
            mediafile = get_object_or_404(MediaFile, id=mediafile_id)
            Content.objects.create(
                playlist=playlist, mediafile=mediafile, duration=duration
            )
        elif custompage_id:
            custompage = get_object_or_404(CustomPage, id=custompage_id)
            Content.objects.create(
                playlist=playlist, custom_page=custompage, duration=duration
            )

        # Render the updated content list
        content_list = playlist.content_set.all()
        html = render_to_string(
            "partials/content_list.html",
            {"playlist": playlist, "contents": content_list},
        )
        return HttpResponse(html)

    return redirect("core:edit_playlist", playlist_id=playlist.id)

@login_required
def delete_content(request, content_id):
    # Fetch the content object
    content = get_object_or_404(Content, id=content_id)
    playlist = content.playlist  # Get the associated playlist

    # Delete the content
    content.delete()

    # Fetch the updated list of contents for the playlist
    content_list = playlist.content_set.all()

    # Render the updated content list as HTML
    html = render_to_string(
        "partials/content_list.html", {"playlist": playlist, "contents": content_list}
    )
    return HttpResponse(html)

@login_required
def displays(request):
    return render(request, "displays.html")


# Browser display for debug and tests
def display_browser(request, playlist_id):
    # Fetch the playlist and its contents
    playlist = get_object_or_404(Playlist, id=playlist_id)
    contents = playlist.content_set.all()

    # Serialize contents to JSON
    contents_json = serialize_contents(contents)

    # Generate a hash of the contents
    content_hash = hashlib.md5(
        "".join(f"{content.id}-{content.duration}" for content in contents).encode(
            "utf-8"
        )
    ).hexdigest()

    # Create the response
    response = render(
        request,
        "display/browser/display_browser.html",
        {
            "playlist": playlist,
            "contents": contents,
            "contents_json": contents_json,
            "content_hash": content_hash,
        },
    )

    # Add the content hash to the response headers
    response["X-Content-Hash"] = content_hash
    return response

def get_video_duration(request, mediafile_id):
    mediafile = get_object_or_404(MediaFile, id=mediafile_id)
    file_path = mediafile.file.path

    # Use ffprobe to get the video duration
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        duration = float(result.stdout.strip())
        return JsonResponse({"duration": int(duration)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
