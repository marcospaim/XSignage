from django.contrib import admin
from core.models import Group, Subgroup, MediaFile, Playlist, Content, Display

# Show guid on admin interface
class DisplayAdmin(admin.ModelAdmin):
    readonly_fields = ('guid',)


# Register your models here.
admin.site.register(Group)
admin.site.register(Subgroup)
admin.site.register(MediaFile)
admin.site.register(Content)
admin.site.register(Playlist)
admin.site.register(Display, DisplayAdmin)
