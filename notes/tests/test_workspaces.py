from django.test import Client, TestCase
from notes.models.note import Note
from notes.models.tag import Tag
from notes.tests.testutils import create_Alice, create_Bob, create_test_workspace


class TestWorkspaces(TestCase):

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

    def test_get_details(self):
        # IF
        self.client.force_login(self.bob)
        another_workspace = create_test_workspace(self.bob.id)

        tag1 = Tag.objects.create(workspace=self.workspace, name='tag1')
        tag2 = Tag.objects.create(workspace=self.workspace, name='tag2')
        tag3 = Tag.objects.create(workspace=another_workspace, name='tag3')

        note1 = Note.objects.create(workspace=self.workspace, title='note1', content='content1')
        note2 = Note.objects.create(workspace=self.workspace, title='note2', content='content2')
        note3 = Note.objects.create(workspace=another_workspace, title='note3', content='content3')
        note1.tags.set([tag1, tag2])
        note1.save()
        note2.tags.set([tag2])
        note2.save()

        # WHEN
        response = self.client.get(f'/api/notes/v1/workspaces/{self.workspace.id}/')

        # THEN
        self.assertEqual(200, response.status_code)
        response_data = response.json()

        note_ids = set([note['id'] for note in response_data['notes']])
        note_titles = set([note['title'] for note in response_data['notes']])
        self.assertEqual(set([note1.id, note2.id]), note_ids)
        self.assertEqual(set([note1.title, note2.title]), note_titles)

        note1 = [note for note in response_data['notes'] if note['id'] == note1.id][0]
        note2 = [note for note in response_data['notes'] if note['id'] == note2.id][0]
        self.assertEqual(set([tag1.id, tag2.id]), set(note1['tags']))
        self.assertEqual(set([tag2.id]), set(note2['tags']))

        tag_ids = set([tag['id'] for tag in response_data['tags']])
        tag_names = set([tag['name'] for tag in response_data['tags']])
        self.assertEqual(set([tag1.id, tag2.id]), tag_ids)
        self.assertEqual(set([tag1.name, tag2.name]), tag_names)

    def test_list_success(self):
        self.client.force_login(self.bob)
        workspace2 = create_test_workspace(self.bob.id)
        alice = create_Alice()
        workspace3 = create_test_workspace(alice.id)

        response = self.client.get(f'/api/notes/v1/workspaces/')

        self.assertEqual(200, response.status_code)
        response_data = response.json()
        self.assertEqual(2, len(response_data))
        self.assertTrue('id' in response_data[0])
        self.assertTrue('name' in response_data[0])
        self.assertTrue('owner' in response_data[0])

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
