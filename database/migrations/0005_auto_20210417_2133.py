# Generated by Django 3.1.5 on 2021-04-17 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_newssite_sitesubscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommend',
            name='history',
        ),
        migrations.AddField(
            model_name='recommend',
            name='similar_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
