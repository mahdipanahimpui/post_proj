# Generated by Django 4.2.4 on 2023-08-25 08:05

import django.core.validators
from django.db import migrations, models
import functools
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=home.models.dir_image_Post, validators=[functools.partial(home.models.validate_max_file_size, *(), **{'max_size': 5242880})]),
        ),
        migrations.AlterField(
            model_name='post',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdfs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), functools.partial(home.models.validate_max_file_size, *(), **{'max_size': 2097152})]),
        ),
        migrations.AlterField(
            model_name='post',
            name='txt_file',
            field=models.FileField(blank=True, null=True, upload_to='txts', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt']), functools.partial(home.models.validate_max_file_size, *(), **{'max_size': 1048576})]),
        ),
        migrations.AlterField(
            model_name='post',
            name='voice_file',
            field=models.FileField(blank=True, null=True, upload_to='voices', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'ogg']), functools.partial(home.models.validate_max_file_size, *(), **{'max_size': 5242880})]),
        ),
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=home.models.dir_image_postImage, validators=[functools.partial(home.models.validate_max_file_size, *(), **{'max_size': 5242880})]),
        ),
    ]
