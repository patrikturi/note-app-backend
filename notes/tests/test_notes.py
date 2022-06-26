from django.test import Client, TestCase
from notes.tests.testutils import create_Alice, create_Bob, create_test_note, create_test_tag, create_test_workspace


class TestNotes(TestCase):

    def setUp(self):
        self.client = Client()
        self.bob = create_Bob()
        self.workspace = create_test_workspace(self.bob.id)
        self.tag1 = create_test_tag(self.workspace)
        self.tag2 = create_test_tag(self.workspace)
        tag3 = create_test_tag(self.workspace)
        self.note = create_test_note(self.workspace)
        self.note.tags.set([self.tag1, self.tag2])
        self.note.save()

    def test_get_success(self):
        self.client.force_login(self.bob)

        response = self.client.get(f'/api/notes/v1/notes/{self.note.id}/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(self.note.id, response_data['id'])
        self.assertEqual('Test note', response_data['title'])
        self.assertEqual('Test note content', response_data['content'])
        self.assertEqual(set([self.tag1.id, self.tag2.id]), set(response_data['tags']))

    def test_create_success(self):
        self.client.force_login(self.bob)

        response = self.client.post('/api/notes/v1/notes/',
            {'title': 'New Note', 'content': 'Note content', 'workspace' : self.workspace.id, 'tags': []}, content_type='application/json')

        self.assertEqual(201, response.status_code)
        response_data = response.json()

        self.assertEqual('New Note', response_data['title'])
        self.assertEqual('Note content', response_data['content'])
        self.assertEqual(self.workspace.id, response_data['workspace'])

    def test_update_success(self):
        self.client.force_login(self.bob)

        response = self.client.patch(f'/api/notes/v1/notes/{self.note.id}/',
            {'tags': [self.tag1.id]}, content_type='application/json')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual([self.tag1.id], response_data['tags'])
        self.note.refresh_from_db()
        self.assertEqual([self.tag1.id], [tag.id for tag in self.note.tags.all()])

    def test_get_denied_without_login(self):

        response = self.client.get(f'/api/notes/v1/tags/{self.note.id}/')

        self.assertEqual(401, response.status_code)

    def test_get_denied_for_other_user(self):
        alice = create_Alice()
        self.client.force_login(alice)

        response = self.client.get(f'/api/notes/v1/notes/{self.note.id}/')

        self.assertEqual(404, response.status_code)
