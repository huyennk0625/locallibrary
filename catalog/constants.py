from django.utils.translation import gettext_lazy as _
# catalog/constants.py

MAX_LENGTH_TITLE = 200
MAX_LENGTH_SUMMARY = 1000
MAX_LENGTH_ISBN = 13
MAX_LENGTH_GENRE_NAME = 200
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_IMPRINT = 200
BOOK_LIST_VIEW_PAGINATE = 10

# BookInstance status choice
LOAN_STATUS_MAINTENANCE = 'm'
LOAN_STATUS_ON_LOAN = 'o'
LOAN_STATUS_AVAILABLE = 'a'
LOAN_STATUS_RESERVED = 'r'

LOAN_STATUS = (
    (LOAN_STATUS_MAINTENANCE, _('Maintenance')),
    (LOAN_STATUS_ON_LOAN, _('On loan')),
    (LOAN_STATUS_AVAILABLE, _('Available')),
    (LOAN_STATUS_RESERVED, _('Reserved')),
)


