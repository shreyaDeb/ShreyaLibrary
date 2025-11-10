from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm
import random

def book_list(request):  
    """Display all books"""
    books = Book.objects.all().order_by('-id')  # Order by latest first
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__icontains=query) |
            Q(tags__icontains=query) |
            Q(publisher__icontains=query)
        )
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        books = books.filter(reading_status=status)
    
    # Filter by tag
    tag = request.GET.get('tag')
    if tag:
        books = books.filter(tags__icontains=tag)
    
    # Limit to latest 36 books only if not searching or filtering
    if not query and not status and not tag:
        books = books[:36]
    
    # Split books into rows of 12 books each for the bookshelf display
    books_per_row = 12
    books_rows = [books[i:i + books_per_row] for i in range(0, len(books), books_per_row)]
    
    context = {
        'books': books,
        'books_rows': books_rows,  # Add this for the template
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
