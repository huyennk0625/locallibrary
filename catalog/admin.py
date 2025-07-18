from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Inline cho BookInstance


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0  # Không hiện sẵn form trống

# Tùy biến hiển thị danh sách Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    # Gộp 2 trường vào một hàng
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Tùy biến hiển thị danh sách Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    # Cho phép thêm/ sửa bản sao trực tiếp từ chi tiết của Book
    inlines = [BooksInstanceInline]

# Đăng ký Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

# Tùy biến hiển thị danh sách BookInstance


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id', 'borrower')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


