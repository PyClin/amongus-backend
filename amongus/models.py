from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from amongus.modelmanagers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=100, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, db_index=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tweets', on_delete=models.CASCADE)
    content = models.TextField()
    flagged = models.BooleanField(default=False, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return f"{self.id} {self.user_id}"


class PatternMapping(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patterns', blank=True, null=True, on_delete=models.CASCADE)
    # tweet - patternmapping one - one relationship
    tweet = models.ForeignKey(Tweet, related_name='patterns', blank=True, null=True, on_delete=models.CASCADE)
    pattern = models.TextField()

    def __str__(self):
        return f"{self.id}"

