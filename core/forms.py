# forms.py
from django import forms
from .models import MediaFile, Playlist, Group, Subgroup


class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ["file"]


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", "group", "subgroup"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set an empty queryset for subgroup initially
        self.fields["subgroup"].queryset = Subgroup.objects.none()

        # If a group is selected, update the subgroup queryset
        if "group" in self.data:
            try:
                group_id = int(self.data.get("group"))
                self.fields["subgroup"].queryset = Subgroup.objects.filter(
                    group_id=group_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["subgroup"].queryset = self.instance.group.subgroup_set.all()


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class SubgroupForm(forms.ModelForm):
    class Meta:
        model = Subgroup
        fields = ["name", "group"]
