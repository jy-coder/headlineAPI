# Generated by Django 3.1.5 on 2021-05-09 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('adv_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('adv_category', models.TextField(blank=True)),
                ('web_link', models.TextField(blank=True)),
                ('img_link', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'Advertisement',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('link', models.CharField(blank=True, max_length=1000, unique=True)),
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
                'db_table': 'Article',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='NewsSite',
            fields=[
                ('site_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('site_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'db_table': 'NewsSite',
            },
        ),
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
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(max_length=1000, unique=True)),
                ('full_name', models.CharField(max_length=1000)),
                ('last_active', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'User',
                'index_together': {('email',)},
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
            name='Subscription',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'Subscription',
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.CreateModel(
            name='SiteSubscription',
            fields=[
                ('site_subscription_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.newssite')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'SiteSubscription',
                'unique_together': {('user', 'site')},
            },
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('recommend_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('recommend_date', models.DateTimeField(auto_now_add=True)),
                ('similar_id', models.IntegerField(blank=True, default=0)),
                ('similar_headline', models.CharField(blank=True, max_length=1000)),
                ('similarity', models.IntegerField(blank=True, default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'Recommend',
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.CreateModel(
            name='ReadingHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('history_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'ReadingHistory',
                'unique_together': {('user', 'article')},
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
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('likes_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('likes_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'Likes',
                'unique_together': {('user', 'article')},
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('bookmark_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.user')),
            ],
            options={
                'db_table': 'Bookmark',
                'unique_together': {('user', 'article')},
            },
        ),
    ]
