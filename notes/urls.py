from django.urls import include, path
from rest_framework import routers
from . import api as myapp_views


router = routers.DefaultRouter()
router.register(r'workspaces', myapp_views.WorkspaceViewset)
router.register(r'tags', myapp_views.TagViewset)
router.register(r'notes', myapp_views.NoteViewset)

urlpatterns = [
    path('', include(router.urls)),
]
