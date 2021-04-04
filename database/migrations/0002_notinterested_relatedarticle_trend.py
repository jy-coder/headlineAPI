# Generated by Django 3.1.5 on 2021-03-27 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('link', models.CharField(blank=True, max_length=1000)),
                ('summary', models.CharField(blank=True, max_length=3000)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.TextField(blank=True)),
                ('keywords', models.CharField(blank=True, max_length=3000)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(blank=True, max_length=100)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Trend',
            },
        ),
        migrations.CreateModel(
            name='RelatedArticle',
            fields=[
                ('related_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('link', models.CharField(blank=True, max_length=1000)),
                ('summary', models.CharField(blank=True, max_length=3000)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.TextField(blank=True)),
                ('keywords', models.CharField(blank=True, max_length=3000)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(blank=True, max_length=100)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
            ],
            options={
                'db_table': 'RelatedArticle',
            },
        ),
        migrations.CreateModel(
            name='NotInterested',
            fields=[
                ('ni_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'NotInterested',
                'unique_together': {('user', 'article')},
            },
        ),
    ]