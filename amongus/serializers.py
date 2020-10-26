from rest_framework import serializers

from amongus.models import Tweet


class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('id', 'content', 'flagged', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self._context.get('request')
        user = request.user
        validated_data['user'] = user

        return super().create(validated_data)
