from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'authors', 'description', 'publisher', 'publish_date',
            'isbn13', 'isbn10', 'pages', 'price', 'tags', 'cover_image',
            'reading_status', 'rating', 'notes'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'authors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author 1, Author 2'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Book description...'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher name'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '13-digit ISBN'}),
            'isbn10': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit ISBN'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of pages'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fiction, classic, adventure'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'reading_status': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Personal notes...'}),
        }