# Generated by Django 3.0 on 2020-05-21 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0014_auto_20200507_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chat_user', models.CharField(blank=True, max_length=255)),
                ('chat_text', models.TextField()),
                ('chat_wrong_intent', models.CharField(blank=True, max_length=256)),
                ('chat_isCorrect', models.BooleanField(default=False)),
                ('chat_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Food',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
