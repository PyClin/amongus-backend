from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from amongus.models import Tweet
from amongus.serializers import TweetCreateSerializer
from amongus.signals import tweet_created, tweet_edited


class TweetListCreateView(ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        tweet = serializer.save()
        tweet_created.send(
            sender=self.__class__, tweet=tweet, request=self.request
        )


class TweetRetrieveUpdateView(RetrieveAPIView, UpdateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        tweet = serializer.save()
        tweet_edited.send(
            sender=self.__class__, tweet=tweet, request=self.request
        )
