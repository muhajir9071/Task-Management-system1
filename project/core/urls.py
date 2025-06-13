from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, project_summary
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet)

projects_router = NestedDefaultRouter(router, 'projects', lookup='project')
projects_router.register('tasks', TaskViewSet, basename='project-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('projects/<int:pk>/summary/', project_summary),
]
