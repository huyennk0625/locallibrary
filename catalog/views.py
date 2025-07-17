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

from django.views import generic
from .models import Book

class BookListView(generic.ListView):
    model = Book
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE
    context_object_name = 'book_list'  # trùng với template mặc định
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['copies'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = constants.LOAN_STATUS_AVAILABLE
        context['STATUS_MAINTENANCE'] = constants.LOAN_STATUS_MAINTENANCE
        context['status_labels'] = dict(constants.LOAN_STATUS)
        return context
