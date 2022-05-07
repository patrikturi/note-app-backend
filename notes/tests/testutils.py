
from notes.models.note import Note
from notes.models.tag import Tag
from notes.models.workspace import Workspace
from registration.models import User


def create_Bob() -> User:
    return User.objects.create_user(username='Bob', email='bob@example.com', password='password')


def create_Alice() -> User:
    return User.objects.create_user(username='Alice', email='alice@example.com', password='password')


def create_test_workspace(user_id: int) -> Workspace:
    return Workspace.objects.create(name='Existing Workspace', owner_id=user_id)


def create_test_tag(workspace: Workspace) -> Tag:
    return Tag.objects.create(workspace=workspace, name='Test tag')


def create_test_note(workspace: Workspace) -> Tag:
    return Note.objects.create(workspace=workspace, title='Test note', content='Test note content')
