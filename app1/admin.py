from django.contrib import admin
from . import models
from .models import StudyContent

admin.site.register(StudyContent)

class stickynotes_admin (admin.ModelAdmin):
    list_display= ('title',)

admin.site.register(models.stickyNote,stickynotes_admin)

admin.site.register(models.Notebook)

