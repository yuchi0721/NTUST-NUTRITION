# Generated by Django 3.0 on 2020-04-09 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='food_num',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
