from django.contrib import admin
from .models import MessageSensibilisation


@admin.register(MessageSensibilisation)
class MessageSensibilisationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_contenu', 'type_message', 'actif', 'created_at']
    list_filter = ['type_contenu', 'type_message', 'actif']
    list_editable = ['actif']
    search_fields = ['titre', 'contenu']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'contenu')
        }),
        ('Configuration', {
            'fields': ('type_contenu', 'type_message', 'actif')
        }),
    )
