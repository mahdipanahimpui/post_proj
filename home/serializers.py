from rest_framework import serializers
from . models import Post, PostImages
import re

class FormatValidator:
    def validate(self, data, exception=None):
        error = {}

        for file, formats in data.items():
            if file:
                file_name = file.name
                file_format = file_name.split('.')[-1]
                if file_format not in formats:
                    error[file_name] = [f'{file_format} not supported:']
        
        if dict:
            raise exception(error)
        
        return True




class PostImgaesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImages
        fields = '__all__'



class PostSerializer(serializers.ModelSerializer):
    images = PostImgaesSerializer(many=True, read_only=True)
    upload_images = serializers.ListField(
        child = serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only  = True, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'phone_number', 'name', 'description', 'image','images', 'upload_images', 'txt_file', 'pdf_file', 'voice_file']


    def validate(self, data):
        files = {
            data.get('txt_file'): ['txt'],
            data.get('pdf_file'): ['pdf'],
            data.get('voice_file'): ['mp3', 'ogg'],
        }

        fm = FormatValidator()
        fm.validate(files, serializers.ValidationError)
        return data
    
    
    def validate_phone_number(self, value):
            pattern = r'^09\d{9}$'
            if not re.match(pattern, value):
                raise serializers.ValidationError('phone_number should be 11 digits, starts with 09')
            return value

    



    def create(self, validated_data):
        uploaded_images = validated_data.pop('upload_images', [])
        post = Post.objects.create(**validated_data)

        for image in uploaded_images:
            PostImages.objects.create(post=post, image=image)

        return post
    

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('upload_images', [])

        for image in uploaded_images:
            PostImages.objects.create(post=instance, image=image)
        return super().update(instance, validated_data)
    


    def delete_all_images(self, instance=None):
        post_images = PostImages.objects.filter(post=instance)
        post_images.delete()


    
    def partial_delete(self, instance, params):
        phone_number = bool(params.get('phone_number', False))
        description = bool(params.get('description', False))
        txt_file = bool(params.get('txt_file', False))
        pdf_file = bool(params.get('pdf_file', False))
        voice_file = bool(params.get('voice_file', False))
        images = params.get('images', '')

        images = images.split(',')
        images = [int(img) for img in images]
        post_images = PostImages.objects.filter(id__in=images)
        post_images.delete()


        data = {
            'phone_number': phone_number,
            'description': description,
            'txt_file': txt_file,
            'pdf_file': pdf_file,
            'voice_file': voice_file,
        }

        for k, v in data.items():
            if v:
                setattr(instance, k, None)

        
        instance.save()
        

            



