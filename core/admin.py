from django.contrib import admin
from core.models import Group, Subgroup, MediaFile

# Register your models here.
admin.site.register(Group)
admin.site.register(Subgroup)
admin.site.register(MediaFile)