from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm
import random

def book_list(request):
    books = Book.objects.all()
    # Add your existing filtering logic here
    
    # Determine books per shelf based on screen size (this will be refined with JavaScript)
    # For initial server-side rendering, we'll use a default value
    books_per_shelf = 18  # Default for larger screens
    
    # Create shelves by splitting books into chunks
    shelves = []
    for i in range(0, len(books), books_per_shelf):
        shelves.append(books[i:i + books_per_shelf])
    
    context = {
        'books': books,
        'shelves': shelves,  # Add this for the template
        'total_books': Book.objects.count(),
        'reading': Book.objects.filter(reading_status='reading').count(),
        'completed': Book.objects.filter(reading_status='completed').count(),
        'wishlist': Book.objects.filter(reading_status='wishlist').count(),
    }
    return render(request, 'books/book_list.html', context)
def book_detail(request, pk):
    """Display single book details"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})

def book_create(request):
    """Create a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'"{book.title}" has been added to your library!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Add'})

def book_update(request, pk):
    """Update existing book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{book.title}" has been updated!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Edit', 'book': book})

def book_delete(request, pk):
    """Delete a book"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" has been removed from your library.')
        return redirect('book_list')
    
    return render(request, 'books/book_confirm_delete.html', {'book': book})

def random_book(request):
    books = Book.objects.filter(reading_status='unread')

    if not books.exists():
        books = Book.objects.exclude(reading_status='wishlist')
        if not books.exists():
            messages.warning(request, "No books available to suggest!")
            return redirect('book_list')

    book = random.choice(books)
    return redirect('book_detail', pk=book.pk)

def my_books(request):
    books = Book.objects.all()

    # Unique authors and tags
    authors = Book.objects.values_list('authors', flat=True).distinct()
    authors = sorted(set(authors))  # ensure uniqueness and sort

    tags = set()
    for book in books:
        tags.update(book.get_tags_list())
    tags = sorted(tags)

    statuses = ['Unread','Reading', 'Completed', 'Wishlist']
    ratings = [1, 2, 3, 4, 5]

    selected_author = request.GET.get('author')
    selected_tag = request.GET.get('tag')
    selected_status = request.GET.get('status')
    selected_rating = request.GET.get('rating')
    sort_by = request.GET.get('sort')

    if selected_author:
        books = books.filter(authors=selected_author)
    if selected_tag:
        books = books.filter(tags__icontains=selected_tag)
    if selected_status:
        books = books.filter(reading_status__iexact=selected_status.lower())
    if selected_rating:
        books = books.filter(rating__gte=int(selected_rating))

    if sort_by == 'title':
        books = books.order_by('title')
    elif sort_by == 'author':
        books = books.order_by('authors')
    elif sort_by == 'rating':
        books = books.order_by('-rating')

    context = {
        'books': books,
        'authors': authors,
        'tags': tags,
        'statuses': statuses,
        'ratings': ratings,
        'selected_author': selected_author,
        'selected_tag': selected_tag,
        'selected_status': selected_status,
        'selected_rating': selected_rating,
        'sort_by': sort_by,
    }
    return render(request, 'books/my_book.html', context)
