from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import MediaFileForm
from .models import MediaFile

def index(request):
    return render(request, "main.html") 
    

def upload_media(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            media_files = MediaFile.objects.all()
            context = {
                'media_files': media_files,
                'message': 'File uploaded successfully!'
            }
            return render(request, "partials/mediafiles-list.html", context)
    media_files = MediaFile.objects.all()

    # Pass the queryset to the template context
    context = {
        'media_files': media_files
    }
    return render(request, "upload_media.html", context)  

def delete_media(request, media_id):
    if request.method == "DELETE":
        media_file = get_object_or_404(MediaFile, id=media_id)
        media_file.delete()
        media_files = MediaFile.objects.all()
        context = {
            'media_files': media_files,
            'message': 'File deleted!'
        }
        return render(request, "partials/mediafiles-list.html", context)

def playlists(request):
    return render(request, "playlists.html")  

def displays(request):
    return render(request, "displays.html")  