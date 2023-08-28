from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from functools import partial
from django.urls import reverse
import re
from django.contrib.sitemaps import ping_google



def dir_image_postImage(instance, filename):
    return f'post_imgs/{instance.post.id}/{filename}'

def dir_image_Post(instance, filename):
    return f'img/{instance.id}-{instance.name}/{filename}'

def validate_max_file_size(value, max_size):
    # max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f"The file size should not exceed {max_size} bytes.")
    
def validate_phone_number(value):
    print('in validation')
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('phone_number should be 11 digits, starting with 09')


class Post(models.Model):
    phone_number = models.CharField(max_length=11, null=True, blank=True, validators=[validate_phone_number])
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True, max_length=512)

    image = models.ImageField(upload_to=dir_image_Post, validators=[
            partial(validate_max_file_size, max_size=5 * 1024 * 1024) # Maximum file size: 5MB
        ])
    
    txt_file = models.FileField(upload_to='txts', blank=True, null=True, validators=[
        FileExtensionValidator(allowed_extensions=['txt']),
            partial(validate_max_file_size, max_size=1 * 1024 * 1024) # Maximum file size: 1MB
    ])
    
    pdf_file = models.FileField(upload_to='pdfs', blank=True, null=True, validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            partial(validate_max_file_size, max_size=2 * 1024 * 1024) # Maximum file size: 2MB
    ])

    voice_file = models.FileField(upload_to='voices', blank=True, null=True, validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'ogg']),
            partial(validate_max_file_size, max_size=5 * 1024 * 1024) # Maximum file size: 5MB
    ])



    def __str__(self):
        return f'{self.id} - {self.name}'
    

    def get_absolute_url(self):
        return f'/home/posts/{self.id}/'
        # return reverse('home:posts', args=(self.id,))

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            print(Exception)
    


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=dir_image_postImage, blank=True, null=True, validators=[
            partial(validate_max_file_size, max_size=5 * 1024 * 1024) # Maximum file size: 5MB
    ])

    def __str__(self):
        return f'{self.id}-{self.post.name} - {self.image}'
    
