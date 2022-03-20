
from notes.models.workspace import Workspace
from users.models import User


def create_Bob() -> User:
    return User.objects.create_user(username='Bob', email='bob@example.com', password='password')


def create_Alice() -> User:
    return User.objects.create_user(username='Alice', email='alice@example.com', password='password')


def create_test_workspace(user_id: int) -> Workspace:
    return Workspace.objects.create(name='Existing Workspace', owner_id=user_id)
