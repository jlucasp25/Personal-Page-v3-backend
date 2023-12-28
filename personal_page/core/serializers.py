from django.core.paginator import Paginator
from rest_framework import serializers

from personal_page.core.models import Activity, Technology, WorkCompany, Project


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class TechnologySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Technology
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class WorkCompanySerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField('paginated_projects')

    class Meta:
        model = WorkCompany
        fields = '__all__'

    def paginated_projects(self, obj):
        projects = obj.projects.all()
        page = self.context['request'].query_params.get('page', 1)
        page_size = self.context['request'].query_params.get('page_size', 2)
        paginator = Paginator(obj.projects.all(), page_size)
        result_page = paginator.get_page(page)
        serializer = ProjectSerializer(result_page, many=True)
        return serializer.data
