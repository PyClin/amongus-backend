import base64
import json
import os
import traceback

import django.db
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.status import is_success

from amongus.models import PatternMapping

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class PatternCreationException(Exception):
    pass


class TypingDnaException(Exception):
    pass


class EmailHelper:
    template_path = os.path.join(settings.BASE_DIR, "amongus/templates/did_you_tweet.html")
    from_email = 'bhaveshpraveen10@gmail.com'

    def get_data(self, **kwargs):
        with open(self.template_path) as f:
            file_content = f.read()

        for key, val in kwargs.items():
            file_content.replace(key, val)

        return file_content

    def send_email(self, email_id, **template_kwargs):
        html_content = self.get_data(**template_kwargs)
        message = Mail(
            from_email=self.from_email,
            to_emails=email_id,
            subject='Did you just tweet?',
            html_content=html_content)
        try:
            sg = SendGridAPIClient(settings.SENDGRID["api_secret"])
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print('Not able to send email:', e)


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
        tp1 = pattern2
        tp2 = pattern1
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

        for _ in range(0, 10):
            try:
                response = requests.post(url, data=data, headers=headers)
                print(f"Response from api: {response.status_code} {response.content}")
                if is_success(response.status_code):
                    return response
                break
            except Exception:
                print(traceback.format_exc())
        return None


class AldiniGraphMSAdapter:
    def add_user(self, user_id, user_name):
        url = f"{settings.ALDINI_MS['url']}/api/add_user/"
        data = {
            'user_id': str(user_id),
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
            'tweet_id': str(tweet_id),
            'user_id': str(user_id),
            'node_number': int(node_number),
            'flagged': flagged
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(
                        f"Added tweet with tweet_id: {tweet_id}; user_id: {user_id}; node_number: {node_number} to Aldini ms")
                    break
                print(
                    f"Failed to add tweet with tweet_id: {tweet_id}; user_id: {user_id}; node_number: {node_number} to Aldini ms")
            except Exception:
                print(traceback.format_exc())

    def edit_tweet(self, tweet_id, flagged=False):
        url = f"{settings.ALDINI_MS['url']}/api/edit_tweet/"
        data = {
            'tweet_id': str(tweet_id),
            'flagged': flagged
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(f"Added tweet with tweet_id: {tweet_id}; flagged: {flagged} to Aldini ms")
                    break
                print(f"Failed to add tweet with tweet_id: {tweet_id}; flagged: {flagged} to Aldini ms")
            except Exception:
                print(traceback.format_exc())

    def add_user_match(self, u1_id, u2_id, confidence):
        url = f"{settings.ALDINI_MS['url']}/api/add_user_match/"
        data = {
            'from_user_id': str(u1_id),
            'to_user_id': str(u2_id),
            'tdna_conf': confidence
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(
                        f"Added user match with user_id: {u1_id}; user_id: {u2_id}; confidence: {confidence} to Aldini ms")
                    break
                print(
                    f"Failed to add user match  user_id: {u1_id}; user_id: {u2_id}; confidence: {confidence} to Aldini ms")
            except Exception as e:
                print(traceback.format_exc())

    def add_tweet_verified(self, user_id, tweet_id, confidence):
        url = f"{settings.ALDINI_MS['url']}/api/add_tweet_verification/"
        data = {
            'user_id': str(user_id),
            'tweet_id': str(tweet_id),
            'tdna_conf': confidence
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(
                        f"Added verified tweet with user_id: {user_id}; tweet_id: {tweet_id}; confidence: {confidence} to Aldini ms")
                    break
                print(
                    f"Failed to add verified tweet with user_id: {user_id}; to_user_id: {tweet_id}; confidence: {confidence} to Aldini ms")
            except Exception as e:
                print(traceback.format_exc())

    def add_tweet_unverified(self, user_id, tweet_id, confidence):
        url = f"{settings.ALDINI_MS['url']}/api/add_tweet_unverification/"
        data = {
            'user_id': str(user_id),
            'tweet_id': str(tweet_id),
            'tdna_conf': confidence
        }
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(
                        f"Added unverified tweet with from_user_id: {user_id}; tweet_id: {tweet_id}; confidence: {confidence} to Aldini ms")
                    break
                print(
                    f"Failed to Add unverified tweet with from_user_id: {user_id}; tweet_id: {tweet_id}; confidence: {confidence} to Aldini ms")
            except Exception as e:
                print(traceback.format_exc())

    def add_tweet_match(self, user_id, tweet_id, tdna_conf):
        url = f"{settings.ALDINI_MS['url']}/api/add_tweet_match/"
        data = {
            'user_id': str(user_id),
            'tweet_id': str(tweet_id),
            'tdna_conf': tdna_conf
        }
        print(f"data={data}")
        headers = {
            "Content-Type": "application/json"
        }
        for _ in range(0, 10):  # max-retry 10 times
            try:
                response = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
                if is_success(response.status_code):
                    print(
                        f"Matched tweet with id {tweet_id} to user_id: {user_id} with confidence: {tdna_conf} to Aldini ms")
                    break
                print(
                    f"Failed to match tweet with id {tweet_id} to user_id: {user_id} with confidence: {tdna_conf} to Aldini ms")
            except Exception as e:
                print(traceback.format_exc())


class BackGroundTypingDnaTaskHelper:

    def on_boarding_typing_pattern_comparison(self, user_id):
        qs = PatternMapping.objects.filter(Q(tweet__isnull=True) &
                                           ~Q(user_id=user_id)).order_by('id')

        new_user = get_user_model().objects.get(id=user_id)
        new_user_pm = new_user.patterns.filter(tweet__isnull=True).first()
        count = qs.count()
        batch_size = 1000
        for start in range(0, count, batch_size):
            end = start + batch_size
            for pm in qs[start:end]:
                response = TypingDnaHelper().send_match_request(pattern1=new_user_pm.pattern, pattern2=pm.pattern)
                if response is None:
                    continue
                content = json.loads(response.content)
                confidence = content.get('confidence')
                if confidence is None:
                    continue
                print(f"Confidence score: {confidence} between user_id: {new_user.id} and user_id: {pm.user_id}")
                try:
                    if content.get("result", 0) >= 1:
                        AldiniGraphMSAdapter().add_user_match(user_id, pm.user_id, confidence)
                except Exception:
                    print(traceback.format_exc())

    def tweet_verfication_success_with_onboarding_pattern(self, user_id: int, tweet_id, confidence):
        try:
            AldiniGraphMSAdapter().add_tweet_verified(user_id, tweet_id, confidence)
        except Exception:
            print(traceback.format_exc())

    def tweet_verification(self, pm, onboarding_pm):
        if not onboarding_pm:
            print(f"Invalid onboarding pattern")
        response = TypingDnaHelper().send_match_request(pm.pattern, onboarding_pm.pattern)
        if not response:
            return
        content = json.loads(response.content)
        result = content.get('result')
        if result is None:
            print(f"Result None")
            return
        print(f"Result score: {result} between pattern mapping: {pm.id} and pattern mapping: {onboarding_pm.user_id}")
        if result == 0:
            self.tweet_verfication_failed_with_onboarding_pattern(pm.user_id, pm.tweet_id, content.get("confidence", 80))
            return
        self.tweet_verfication_success_with_onboarding_pattern(pm.user_id, pm.tweet_id, content.get("confidence", 80))

    def tweet_verfication_failed_with_onboarding_pattern(self, user_id, tweet_id, confidence):
        try:
            AldiniGraphMSAdapter().add_tweet_unverified(user_id, tweet_id, confidence)
            # todo: send email here
        except Exception:
            print(traceback.format_exc())

    def compare_tweet_with_all_onboarding_tweets(self, tweet):
        qs = PatternMapping.objects.filter(
            Q(tweet__isnull=True) &
            ~Q(user_id=tweet.user_id)
        ).order_by('id')
        count = qs.count()
        batch_size = 1000
        tweet_pm = tweet.patterns.first()
        if not tweet_pm:
            print("There is not tweet pm")
            return

        for start in range(0, count, batch_size):
            end = start + batch_size
            for pm in qs[start:end]:
                response = TypingDnaHelper().send_match_request(pattern1=tweet_pm.pattern, pattern2=pm.pattern)
                if not response:
                    continue
                content = json.loads(response.content)
                result = content.get('result', 0)
                if not result:
                    continue
                print(f"Result score: {result} between user_id: {pm.user_id} and user_id: {tweet_pm.user_id}")
                try:
                    AldiniGraphMSAdapter().add_tweet_match(pm.user_id, tweet.id, content.get("confidence", 80))
                except Exception:
                    print(traceback.format_exc())
