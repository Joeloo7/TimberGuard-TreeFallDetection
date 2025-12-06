from django.contrib import admin
from . import models

class display(admin.ModelAdmin):
    list_display=('flnm',)
admin.site.register(models.usruploads,display)

# Register your models here.
