# Generated by Django 5.1.3 on 2024-11-18 09:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_blogpost_delete_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]