from django.test import Client, TestCase
from notes.tests.testutils import create_Alice, create_Bob, create_test_tag, create_test_workspace


class TestTags(TestCase):

    def setUp(self):
        self.client = Client()
        self.bob = create_Bob()
        self.workspace = create_test_workspace(self.bob.id)
        self.tag = create_test_tag(self.workspace)

    def test_get_success(self):
        self.client.force_login(self.bob)

        response = self.client.get(f'/api/notes/v1/tags/{self.tag.id}/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(self.tag.id, response_data['id'])
        self.assertEqual('Test tag', response_data['name'])

    def test_list_success(self):
        self.client.force_login(self.bob)
        tag2 = create_test_tag(self.workspace)
        workspace2 = create_test_workspace(self.bob.id)
        tag3 = create_test_tag(workspace2)
        alice = create_Alice()
        workspace3 = create_test_workspace(alice.id)
        tag4 = create_test_tag(workspace3)

        response = self.client.get(f'/api/notes/v1/tags/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(3, len(response_data))
        self.assertTrue('id' in response_data[0])
        self.assertTrue('name' in response_data[0])

    def test_create_success(self):
        self.client.force_login(self.bob)

        response = self.client.post('/api/notes/v1/tags/',
            {'name': 'New Tag', 'workspace': self.workspace.id}, content_type='application/json')

        self.assertEqual(201, response.status_code)
        response_data = response.json()

        self.assertEqual('New Tag', response_data['name'])
        self.assertEqual(self.workspace.id, response_data['workspace'])

    def test_update_success(self):
        self.client.force_login(self.bob)

        response = self.client.patch(f'/api/notes/v1/tags/{self.tag.id}/',
            {'name': 'Another Name'}, content_type='application/json')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual('Another Name', response_data['name'])
        self.assertEqual(self.workspace.id, response_data['workspace'])
        self.tag.refresh_from_db()
        self.assertEqual('Another Name', self.tag.name)

    def test_get_denied_without_login(self):

        response = self.client.get(f'/api/notes/v1/tags/{self.tag.id}/')

        self.assertEqual(401, response.status_code)

    def test_get_denied_for_other_user(self):
        alice = create_Alice()
        self.client.force_login(alice)

        response = self.client.get(f'/api/notes/v1/tags/{self.tag.id}/')

        self.assertEqual(404, response.status_code)
