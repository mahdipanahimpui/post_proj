from django.db import models


def dir_image_postImage(instance, filename):
    return f'post_imgs/{instance.post.id}/{filename}'

def dir_image_Post(instance, filename):
    return f'img/{instance.id}-{instance.name}/{filename}'


class Post(models.Model):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True, max_length=512)
    image = models.ImageField(upload_to=dir_image_Post)
    txt_file = models.FileField(upload_to='txts', blank=True, null=True)
    pdf_file = models.FileField(upload_to='pdfs', blank=True, null=True)
    voice_file = models.FileField(upload_to='voices', blank=True, null=True)\
    



    def __str__(self):
        return f'{self.id} - {self.name}'
    


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=dir_image_postImage, blank=True, null=True)

    def __str__(self):
        return f'{self.id}-{self.post.name} - {self.image}'