from django.test import Client, TestCase
from notes.tests.test_utils import create_Alice, create_Bob, create_test_workspace


class TestWorkspace(TestCase):

    def setUp(self):
        self.client = Client()
        self.bob = create_Bob()
        self.workspace = create_test_workspace(self.bob.id)

    def test_get_success(self):
        self.client.force_login(self.bob)

        response = self.client.get(f'/api/notes/v1/workspaces/{self.workspace.id}/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(self.workspace.id, response_data['id'])
        self.assertEqual('Existing Workspace', response_data['name'])
        self.assertEqual(self.bob.id, response_data['owner'])

    def test_create_success(self):
        self.client.force_login(self.bob)

        response = self.client.post('/api/notes/v1/workspaces/',
            {'name': 'New Workspace', 'owner': self.bob.id}, content_type='application/json')

        self.assertEqual(201, response.status_code)
        response_data = response.json()

        self.assertEqual('New Workspace', response_data['name'])
        self.assertEqual(self.bob.id, response_data['owner'])

    def test_replace_success(self):
        self.client.force_login(self.bob)
        alice = create_Alice()

        response = self.client.put(f'/api/notes/v1/workspaces/{self.workspace.id}/',
            {'name': 'Another Name', 'owner': alice.id}, content_type='application/json')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual('Another Name', response_data['name'])
        self.assertEqual(alice.id, response_data['owner'])
        self.workspace.refresh_from_db()
        self.assertEqual('Another Name', self.workspace.name)
        self.assertEqual(alice.id, self.workspace.owner_id)

    def test_update_success(self):
        self.client.force_login(self.bob)

        response = self.client.patch(f'/api/notes/v1/workspaces/{self.workspace.id}/',
            {'name': 'Another Name'}, content_type='application/json')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual('Another Name', response_data['name'])
        self.workspace.refresh_from_db()
        self.assertEqual('Another Name', self.workspace.name)

    def test_get_denied_without_login(self):

        response = self.client.get(f'/api/notes/v1/workspaces/{self.workspace.id}/')

        self.assertEqual(403, response.status_code)

    def test_get_denied_for_other_user(self):
        alice = create_Alice()
        self.client.force_login(alice)

        response = self.client.get(f'/api/notes/v1/workspaces/{self.workspace.id}/')

        self.assertEqual(404, response.status_code)

# TODO: get with notes/tags
