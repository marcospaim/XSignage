from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subgroup(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["name", "group"],
                name="unique_name_group",
            )
        ]

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


class CustomPage(models.Model):
    view_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.view_name


class Content(models.Model):
    TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
        ("view", "External View"),
    ]

    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, editable=False)
    mediafile = models.ForeignKey(
        "MediaFile", on_delete=models.CASCADE, null=True, blank=True
    )
    custom_page = models.ForeignKey(
        CustomPage, on_delete=models.CASCADE, null=True, blank=True
    )  # Reference to CustomPage

    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(3600)]
    )

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-detect content type
        if self.mediafile:
            # Check file extension for image or video
            file_extension = self.mediafile.file.name.split(".")[-1].lower()
            if file_extension in ["jpg", "jpeg", "png", "gif", "webp"]:
                self.content_type = "image"
            elif file_extension in ["mp4", "mov", "avi", "mkv"]:
                self.content_type = "video"
        elif self.custom_page:
            self.content_type = "view"
        else:
            raise ValueError(
                "Content must have a media file or a custom page reference."
            )

        super().save(*args, **kwargs)

    def __str__(self):
        if self.content_type == "view":
            return f"External View: {self.custom_page.view_name}"
        return f"{self.playlist.name} - {self.mediafile or self.custom_page}"

    def is_active(self):
        now = timezone.now()

        # Handle missing values
        if not self.start_time and not self.end_time:
            raise ValidationError(
                "Both start_time and end_time are missing. Cannot determine active status."
            )

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError(
                "start_time cannot be greater than or equal to end_time."
            )

        # Active logic with appropriate defaults
        start_condition = not self.start_time or self.start_time <= now
        end_condition = not self.end_time or now <= self.end_time

        return start_condition and end_condition


# Display
