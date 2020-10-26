import base64
import json
import traceback

import django.db
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.status import is_success

from amongus.models import PatternMapping


class PatternCreationException(Exception):
    pass


class PatternHelper:

    def create_tweet_pattern(self, tweet, pattern):
        user = tweet.user

        try:
            obj = PatternMapping.objects.create(
                user=user,
                tweet=tweet,
                pattern=pattern
            )
            print(f"Created user tweet pattern in PatternMapping model")
        except django.db.Error:
            print(traceback.format_exc())
            raise PatternCreationException

        return obj

    def create_user_reg_pattern(self, user, pattern):
        try:
            obj = PatternMapping.objects.create(
                user=user,
                pattern=pattern
            )
            print(f"Created user: {user.id} onboarding pattern in PatternMapping model")
        except django.db.Error:
            print(traceback.format_exc())
            raise PatternCreationException

        return obj


class TypingDnaHelper:
    base_url = "https://api.typingdna.com"

    def send_match_request(self, pattern1, pattern2):
        url = f'{self.base_url}/match'
        api_key = settings.TYPING_DNA['api_key']
        api_secret = settings.TYPING_DNA['api_secret']
        tp1 = pattern1
        tp2 = pattern2
        quality = '2'

        authstring = '%s:%s' % (api_key, api_secret)
        # base64string = base64.encodebytes(authstring.encode()).decode().replace()
        base64string = base64.encodestring(authstring.encode()).decode().replace('\n', '')

        headers = {
            'Authorization': f'Basic {base64string}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'tp1': tp1,
            'tp2': tp2,
            'quality': quality
        }

        response = requests.post(url, data=data, headers=headers)


class AldiniGraphMSAdapter:
    def add_user(self, user_id, user_name):
        url = f"{settings.ALDINI_MS['url']}/api/add_user/"
        data = {
            'user_id': user_id,
            'user_name': user_name
        }
        headers = {
            "Content-Type": "application/json"
        }
        for i in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(f"Added user with user_id {user_id} to Aldini ms")
                    break
                print(f"Failed to add user with user_id: {user_id} to Aldini ms")
            except Exception:
                print(traceback.format_exc())

    def add_tweet(self, tweet_id, user_id, node_number, flagged=False):
        url = f"{settings.ALDINI_MS['url']}/api/add_tweet/"
        data = {
            'tweet_id': tweet_id,
            'user_id': user_id,
            'node_number': node_number,
            'flagged': flagged
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(f"Added tweet with tweet_id: {tweet_id}; user_id: {user_id}; node_number: {node_number} to Aldini ms")
                    break
                print(f"Failed to add tweet with tweet_id: {tweet_id}; user_id: {user_id}; node_number: {node_number} to Aldini ms")
            except Exception:
                print(traceback.format_exc())

    def edit_tweet(self, tweet_id, flagged=False):
        url = f"{settings.ALDINI_MS['url']}/api/edit_tweet/"
        data = {
            'tweet_id': tweet_id,
            'flagged': flagged
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(f"Added tweet with tweet_id: {tweet_id}; flagged: {flagged } to Aldini ms")
                    break
                print(f"Failed to add tweet with tweet_id: {tweet_id}; flagged: {flagged} to Aldini ms")
            except Exception:
                print(traceback.format_exc())
