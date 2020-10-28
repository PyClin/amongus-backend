import traceback

from celery import shared_task
from django.contrib.auth import get_user_model

from amongus.models import Tweet, PatternMapping
from amongus.utils import PatternHelper, AldiniGraphMSAdapter, BackGroundTypingDnaTaskHelper


@shared_task
def add_user_to_aldini_ms(user_id, username):
    try:
        AldiniGraphMSAdapter().add_user(user_id, username)
    except Exception:
        print(traceback.format_exc())


@shared_task
def post_user_creation_tasks(user_id: int, pattern: str):
    user = get_user_model().objects.get(id=user_id)

    add_user_to_aldini_ms(user.id, user.username)
    PatternHelper().create_user_reg_pattern(
        user=user,
        pattern=pattern
    )
    BackGroundTypingDnaTaskHelper().on_boarding_typing_pattern_comparison(user_id)


@shared_task
def add_tweet_to_aldini_ms(tweet_id, user_id):
    node_number = PatternMapping.objects.filter(
        user_id=user_id,
        tweet_id=tweet_id
    ).count()
    try:
        AldiniGraphMSAdapter().add_tweet(tweet_id, user_id, node_number)
    except Exception:
        print(traceback.format_exc())


@shared_task
def tweet_pattern_check(tweet_id: int):
    tweet = Tweet.objects.get(id=tweet_id)
    user = tweet.user
    pm = tweet.patterns.first()
    onboarding_pm = user.patterns.filter(tweet__isnull=True).first()
    BackGroundTypingDnaTaskHelper().tweet_verification(
        pm,
        onboarding_pm
    )


@shared_task
def all_users_tweet_matching(tweet_id: int):
    tweet = Tweet.objects.get(id=tweet_id)
    BackGroundTypingDnaTaskHelper().compare_tweet_with_all_onboarding_tweets(tweet)

@shared_task
def post_tweet_creation_tasks(tweet_id: int, pattern: str):
    tweet = Tweet.objects.get(id=tweet_id)
    add_tweet_to_aldini_ms(tweet_id, tweet.user_id)
    PatternHelper().create_tweet_pattern(
        tweet=tweet,
        pattern=pattern
    )
    tweet_pattern_check.delay(tweet_id=tweet.id)
    all_users_tweet_matching.delay(tweet_id=tweet.id)



@shared_task
def post_tweet_editing_tasks(tweet_id: int, flagged: bool):
    try:
        AldiniGraphMSAdapter().edit_tweet(tweet_id, flagged=flagged)
    except Exception:
        print(traceback.format_exc())
