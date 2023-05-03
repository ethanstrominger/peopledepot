from django.urls import path
from rest_framework import routers

from .practice_area_views import PracticeAreaViewSet


def register(router: routers.SimpleRouter):
    router.register(r"practice-areas", PracticeAreaViewSet, basename="practice-area")
