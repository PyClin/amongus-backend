# Generated by Django 3.1.2 on 2020-10-31 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amongus', '0002_patternmapping_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, db_index=True, default='', max_length=100, verbose_name='email_id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='username'),
        ),
    ]
