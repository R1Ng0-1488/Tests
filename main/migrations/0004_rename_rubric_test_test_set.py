# Generated by Django 3.2.2 on 2021-05-23 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210523_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='rubric',
            new_name='test_set',
        ),
    ]
