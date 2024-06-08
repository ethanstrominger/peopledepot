from django.urls import path
from core.api.custom_token_api import CustomTokenObtainView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AffiliateViewSet
from .views import AffiliationViewSet
from .views import EventViewSet
from .views import FaqViewedViewSet
from .views import FaqViewSet
from .views import LocationViewSet
from .views import PermissionTypeViewSet
from .views import PracticeAreaViewSet
from .views import ProgramAreaViewSet
from .views import ProjectViewSet
from .views import SdgViewSet
from .views import SkillViewSet
from .views import StackElementTypeViewSet
from .views import TechnologyViewSet
from .views import UserProfileAPIView
from .views import UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"events", EventViewSet, basename="event")
router.register(r"practice-areas", PracticeAreaViewSet, basename="practice-area")
router.register(r"affiliates", AffiliateViewSet, basename="affiliate")
router.register(r"faqs", FaqViewSet, basename="faq")
router.register(r"faqs-viewed", FaqViewedViewSet, basename="faq-viewed")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"program-areas", ProgramAreaViewSet, basename="program-area")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(r"technologies", TechnologyViewSet, basename="technology")
router.register(r"permission-types", PermissionTypeViewSet, basename="permission-type")
router.register(
    r"stack-element-types", StackElementTypeViewSet, basename="stack-element-type"
)
router.register(r"sdgs", SdgViewSet, basename="sdg")
router.register(
    r"affiliations",
    AffiliationViewSet,
    basename="affiliation",
)
urlpatterns = [
    path("me/", UserProfileAPIView.as_view(), name="my_profile"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CustomTokenObtainView.as_view(), name='token_obtain'),

]

urlpatterns += router.urls
