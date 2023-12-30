from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from personal_page.core.viewsets import ActivityViewSet, TechnologyViewSet, WorkCompanyViewSet, ProjectViewSet, \
    LectureViewSet
from personal_page.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

router.register("activities", ActivityViewSet)

router.register("tech-stack", TechnologyViewSet)

router.register("work", WorkCompanyViewSet)
router.register("projects", ProjectViewSet)
router.register('lectures', LectureViewSet)
app_name = "api"
urlpatterns = router.urls
