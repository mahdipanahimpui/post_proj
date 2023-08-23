from rest_framework import serializers
from . models import Post, PostImages



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


    def create(self, validated_data):
        uploaded_images = validated_data.pop('upload_images')
        post = Post.objects.create(**validated_data)

        for image in uploaded_images:
            PostImages.objects.create(post=post, image=image)

        return post
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('upload_images')

        for image in uploaded_images:
            PostImages.objects.create(post=instance, image=image)
        return super().update(instance, validated_data)
    

    def update_uploaded_images(self, post_instance, validated_data):
        



