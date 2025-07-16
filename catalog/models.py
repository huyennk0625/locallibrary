from django.db import models
from django.urls import reverse
import uuid  # for unique BookInstance IDs
from . import constants  # constants file
from django.utils.translation import gettext_lazy as _

class Genre(models.Model):

    """Model representing a book genre."""
    name = models.CharField(
        max_length=constants.MAX_LENGTH_GENRE_NAME,
        help_text=_('Enter a book genre (e.g. Science Fiction)'))

    def __str__(self):
        return self.name  # Lấy tên thể loại của sách


class Book(models.Model):

    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=constants.MAX_LENGTH_SUMMARY,
        help_text=_('Enter a brief description of the book'))
    isbn = models.CharField(
        _('ISBN'),
        max_length=constants.MAX_LENGTH_ISBN,
        unique=True,
        help_text=(_('13 Character '
                   '<a href="https://www.isbn-international.org/content/'
                   'what-isbn">ISBN number</a>'))
    )  # Mã số của sách, unique
    genre = models.ManyToManyField(
        Genre,
        help_text=_('Select a genre for this book'))  # Book 0..* 1..* Genre

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # id ngầm autofield, tăng tự động.
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for Genre.
        This is required to display genre is Admin."""
        return ','.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = _('Genre')


class BookInstance(models.Model):

    """Model representing a specific copy of a book
    (i.e. that can be borrowed from the library).
    Bản sao cụ thể của một cuốn sách (ví dụ: có thể mượn)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_('Unique ID for this book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=constants.MAX_LENGTH_IMPRINT)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=constants.LOAN_STATUS,
        blank=True,
        default=constants.LOAN_STATUS_MAINTENANCE,
        help_text=_('Book availability'),
    )

    class Meta:
        # Sắp xếp theo hạn trả
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):

    """Model representing an author."""
    first_name = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR_NAME)
    last_name = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(_('Died'), null=True, blank=True)

    class Meta:
        # Sắp xếp theo tên
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
