from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Create_task)
class Create_taskAdmin(admin.ModelAdmin):
    list_display=['user','title','status','start_date','end_date','is_completed','is_deleted']


@admin.register(Assign_task)
class Assign_taskAdmin(admin.ModelAdmin):
    list_display=['assign_to','title','deadline']