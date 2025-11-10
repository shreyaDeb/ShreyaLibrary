from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'publisher', 'publish_date', 'reading_status', 'rating', 'date_added']
    list_filter = ['reading_status', 'rating', 'publisher', 'publish_date']
    search_fields = ['title', 'authors', 'isbn13', 'isbn10', 'tags']
    readonly_fields = ['date_added', 'last_modified']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'authors', 'description')
        }),
        ('Publishing Information', {
            'fields': ('publisher', 'publish_date', 'isbn13', 'isbn10')
        }),
        ('Book Details', {
            'fields': ('pages', 'price', 'tags', 'cover_image')
        }),
        ('Personal Information', {
            'fields': ('reading_status', 'rating', 'notes')
        }),
        ('Metadata', {
            'fields': ('date_added', 'last_modified'),
            'classes': ('collapse',)
        }),
    )