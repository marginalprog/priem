# Generated by Django 4.2.4 on 2024-01-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_form_filled',
            field=models.BooleanField(default=False),
        ),
    ]