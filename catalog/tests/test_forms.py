import datetime
from django.test import TestCase
from django.utils import timezone
from catalog.forms import RenewBookForm
from django.utils.translation import gettext_lazy as _
from catalog import constants

ONE_DAY = datetime.timedelta(days=1)


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label in [
                        None, _('renewal date')])

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            _('Enter a date between now and 4 weeks (default 3).'))

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - ONE_DAY
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = (datetime.date.today() +
                datetime.timedelta(weeks=constants.MAX_RENEWAL_WEEKS) +
                ONE_DAY)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = (datetime.date.today() +
                datetime.timedelta(weeks=constants.MAX_RENEWAL_WEEKS))
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
