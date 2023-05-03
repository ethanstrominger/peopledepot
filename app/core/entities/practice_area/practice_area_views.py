from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import PracticeArea

from .practice_area_serializers import PracticeAreaSerializer


class PracticeAreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PracticeArea.objects.all()
    serializer_class = PracticeAreaSerializer
