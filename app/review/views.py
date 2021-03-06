from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Review
from review import serializers


class ReviewViewSet(viewsets.ModelViewSet):
    """Manage reviews in the database"""
    serializer_class = serializers.ReviewSerializer
    queryset = Review.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the reviews for authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Creates a new review"""
        serializer.save(user=self.request.user)
