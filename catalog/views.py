from django.shortcuts import render
from django.utils.translation import gettext as _
from catalog.models import Book, Author, BookInstance, Genre
from catalog import constants


def index(request):
    """View function for home page of site."""

    # Đếm số lượng bản ghi trong các bảng
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Đếm số lượng sách còn sẵn sàng mượn (status = available)
    num_instances_available = BookInstance.objects.filter(
        status__exact=constants.LOAN_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    # Dữ liệu truyền vào template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Trả về template đã render
    return render(request, 'index.html', context=context)
