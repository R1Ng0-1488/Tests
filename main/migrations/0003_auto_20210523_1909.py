# Generated by Django 3.2.2 on 2021-05-23 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_rubric_testset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='test',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]