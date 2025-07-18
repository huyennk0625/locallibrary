from django.views import generic
from .models import Book
from django.shortcuts import render
from django.utils.translation import gettext as _
from catalog.models import Book, Author, BookInstance, Genre
from catalog import constants
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    """View function for home page of site."""

    # Đếm số lượng bản ghi trong các bảng
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Đếm số lượng sách còn sẵn sàng mượn (status = available)
    num_instances_available = BookInstance.objects.filter(
        status__exact=constants.LOAN_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    # Lấy số lượt truy cập từ session (mặc định là 1)
    num_visits = request.session.get('num_visits', 1)

    # Cập nhật giá trị đó và lưu lại
    request.session['num_visits'] = num_visits + 1

    # Dữ liệu truyền vào template
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Trả về template đã render
    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE
    context_object_name = 'book_list'  # trùng với template mặc định
    template_name = 'catalog/book_list.html'


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['copies'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = constants.LOAN_STATUS_AVAILABLE
        context['STATUS_MAINTENANCE'] = constants.LOAN_STATUS_MAINTENANCE
        context['status_labels'] = dict(constants.LOAN_STATUS)
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = constants.LOAN_BOOKS_BY_USER_LIST_VIEW_PAGINATE

    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(borrower=self.request.user)
            .filter(status__exact=constants.LOAN_STATUS_ON_LOAN)
            .order_by('due_back')
        )


@permission_required('catalog.can_mark_returned')
def mark_book_returned(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = constants.LOAN_STATUS_AVAILABLE
    book_instance.save()
    return redirect('my-borrowed')
