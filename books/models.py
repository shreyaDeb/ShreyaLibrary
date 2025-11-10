from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os

def book_cover_path(instance, filename):
    """Generate upload path for book covers"""
    ext = filename.split('.')[-1]
    filename = f"{instance.isbn13 or instance.isbn10 or 'book'}_{instance.id}.{ext}"
    return os.path.join('covers', filename)

class Book(models.Model):
    # Basic Information
    title = models.CharField(max_length=500)
    authors = models.CharField(max_length=500, help_text="Separate multiple authors with commas")
    description = models.TextField(blank=True)
    
    # Publishing Information
    publisher = models.CharField(max_length=200, blank=True)
    publish_date = models.DateField(null=True, blank=True)
    
    # ISBN Information
    isbn13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    isbn10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    # Book Details
    pages = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Additional Information
    tags = models.CharField(max_length=500, blank=True, help_text="Separate tags with commas")
    cover_image = models.ImageField(upload_to=book_cover_path, blank=True, null=True)
    
    # Metadata
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    # Reading Status
    READING_STATUS = [
        ('unread', 'Unread'),
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('wishlist', 'Wishlist'),
    ]
    reading_status = models.CharField(max_length=20, choices=READING_STATUS, default='unread')
    
    # Rating
    rating = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 to 5 stars"
    )
    
    # Personal Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return self.title
    
    def get_authors_list(self):
        """Return authors as a list"""
        return [author.strip() for author in self.authors.split(',') if author.strip()]
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]