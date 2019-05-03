from rest_framework import serializers
from core.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer a review"""

    class Meta:
        model = Review
        fields = ('id', 'title', 'rating', 'summary', 'ip_address',
                  'submission_date', 'company')
        read_only_fields = ['id', ]

    def create(self, validated_data):
        request = self.context.get('request')
        remote_id = request.META['REMOTE_ADDR']
        validated_data['ip_address'] = remote_id

        return super().create(validated_data)
