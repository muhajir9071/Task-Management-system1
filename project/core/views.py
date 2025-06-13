

# Create your views here.
from rest_framework import viewsets, filters
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.db.models import Count

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.all()
        project_id = self.kwargs.get('project_pk')

        if project_id:
            queryset = queryset.filter(project__id=project_id)

        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to:
            queryset = queryset.filter(assigned_to__username=assigned_to)

        if self.request.query_params.get('due_today') == 'true':
            queryset = queryset.filter(due_date=date.today())

        return queryset

# Project Summary View
from rest_framework.decorators import api_view
@api_view(['GET'])
def project_summary(request, pk):
    data = Task.objects.filter(project_id=pk).values('status').annotate(count=Count('status'))
    return Response({item['status']: item['count'] for item in data})
