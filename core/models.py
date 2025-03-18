from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Subgroup(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class MediaFile(models.Model):
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subgroup = models.ForeignKey(
        Subgroup,
        on_delete=models.CASCADE,
        null=True,
    )

class Content(models.Model):
    mediafile = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3600)])

#Display