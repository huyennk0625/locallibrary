from django.test import TestCase
from django.urls import reverse
from catalog.models import Author
from catalog import constants


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for author_id in range(constants.NUM_TEST_AUTHORS):
            Author.objects.create(first_name=f'Christian {author_id}',
                                  last_name=f'Surname {author_id}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(
            len(response.context['author_list']), constants.PAGINATION_LIMIT)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(
            len(response.context['author_list']),
            constants.NUM_TEST_AUTHORS - constants.PAGINATION_LIMIT)
