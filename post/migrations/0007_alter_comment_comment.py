# Generated by Django 4.2.3 on 2024-10-14 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
