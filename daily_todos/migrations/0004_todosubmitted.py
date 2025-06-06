# Generated by Django 5.2.1 on 2025-06-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_todos', '0003_datetodos_key_alter_livetodo_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoSubmitted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('submitted_time', models.DateTimeField()),
                ('date_todos', models.JSONField()),
                ('live_todos', models.JSONField()),
            ],
        ),
    ]
