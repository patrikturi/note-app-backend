from django.test import Client, TestCase
from notes.tests.test_utils import create_Alice, create_Bob, create_test_workspace


class TestWorkspace(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_Bob()

    def test_get_success(self):
        workspace = create_test_workspace(self.user.id)

        response = self.client.get(f'/api/notes/v1/workspaces/{workspace.id}/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(workspace.id, response_data['id'])
        self.assertEqual('Existing Workspace', response_data['name'])
        self.assertEqual(self.user.id, response_data['owner'])

    def test_create_success(self):
        response = self.client.post('/api/notes/v1/workspaces/',
            {'name': 'New Workspace', 'owner': self.user.id}, content_type='application/json')

        self.assertEqual(201, response.status_code)
        response_data = response.json()

        self.assertEqual('New Workspace', response_data['name'])
        self.assertEqual(self.user.id, response_data['owner'])

    def test_update_success(self):
        alice = create_Alice()
        workspace = create_test_workspace(self.user.id)

        response = self.client.put(f'/api/notes/v1/workspaces/{workspace.id}/',
            {'name': 'Another Name', 'owner': alice.id}, content_type='application/json')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual('Another Name', response_data['name'])
        self.assertEqual(alice.id, response_data['owner'])
        workspace.refresh_from_db()
        self.assertEqual('Another Name', workspace.name)
        self.assertEqual(alice.id, workspace.owner_id)
