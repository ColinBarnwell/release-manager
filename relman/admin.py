from django.contrib import admin

from models import Checkpoint


class CheckpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = 'display_order',


admin.site.register(Checkpoint, CheckpointAdmin)
