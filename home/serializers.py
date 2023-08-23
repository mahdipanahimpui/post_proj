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

        data = {
            'phone_number': phone_number,
            'description': description,
            'txt_file': txt_file,
            'pdf_file': pdf_file,
            'voice_file': voice_file,
        }

        images = params.get('images', '')
        images = images.split(',')

        images = [int(img) for img in images]
        post_images = PostImages.objects.filter(id__in=images)
        post_images.delete()


        for k, v in data.items():
            if v:
                setattr(instance, k, None)

        
        instance.save()
        

            



