from django.contrib import admin
from .models import Batch, BatchItem

class BatchItemInline(admin.TabularInline):
    model = BatchItem
    extra = 1

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'arrival_date', 'status', 'created_at')
    inlines = [BatchItemInline]