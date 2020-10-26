from django.dispatch import receiver, Signal
from djoser.signals import user_registered

from amongus.tasks import post_user_creation_tasks, post_tweet_creation_tasks, post_tweet_editing_tasks

# signals
tweet_created = Signal()
tweet_edited = Signal()


@receiver(user_registered)
def user_registered_callback(sender, user, request, **kwargs):
    data = request.data
    pattern = data.get('pattern')
    print(f"data: {data}")
    print(f"Pattern: {pattern}")
    if not pattern:
        return
    post_user_creation_tasks.delay(user.id, pattern)


@receiver(tweet_created)
def tweet_created_callback(sender, tweet, request, **kwargs):
    if sender.__name__ == 'TweetListCreateView':
        pattern = request.data.get("pattern")
        if not pattern:
            return
        post_tweet_creation_tasks.delay(tweet.id, pattern)


@receiver(tweet_edited)
def tweet_edited_callback(sender, tweet, request, **kwargs):
    if sender.__name__ == 'TweetRetrieveUpdateView':
        flagged = request.data.get("flagged")
        if not flagged:
            return
        post_tweet_editing_tasks.delay(tweet.id, flagged)
