from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from personal_page.core.models import Activity, Technology, WorkCompany, Project, Lecture
from personal_page.core.serializers import ActivitySerializer, TechnologySerializer, WorkCompanySerializer, \
    ProjectSerializer, LectureSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(active=True)
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.filter(active=True)
    serializer_class = TechnologySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.GET.__contains__('inactive'):
            return Technology.objects.filter(active=False)
        return Technology.objects.filter(active=True)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    page_size = 2


class WorkCompanyViewSet(viewsets.ModelViewSet):
    queryset = WorkCompany.objects.all()
    serializer_class = WorkCompanySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    page_size = 2

    def get_queryset(self):
        if 'freelance' in self.request.GET:
            return WorkCompany.objects.filter(freelance=True)
        return WorkCompany.objects.filter(freelance=False)

class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [permissions.AllowAny]