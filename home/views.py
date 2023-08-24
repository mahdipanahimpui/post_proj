from django.shortcuts import render
from django.views import View
from django.shortcuts import HttpResponse
from rest_framework import viewsets
from . models import Post, PostImages
from . serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status




# class Home(View):
#     def get(self, request):
#         return HttpResponse('home page')



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        """
                retrieve: used to get one element
            Note: upload images is just writable

        """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
                create: used to create post object
                fields are: name, phone_number, description, image, upload_images, txt_file, pdf_file, voice_file
                name and image is required to create and update
            validation param: 
            
                > file format suported: {pdf_file: pdf} {txt_file: txt} {voice_file: mp3, ogg} {image,images: png,jpeg,jpg}
                > phone_number: just number, 11 digit, start with 09
                > name: charField, max_length=128
                > description: textField, max_length=256
                > upload_images: max_length=100000
        """
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        """
                list: lists the fields
                fields contains: name, phone_number, description, image, images{id, image, post_id}, txt_file, pdf_file, voice_file
            Note: upload images is just writable
        """
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
                delete : destroy the post object. 
                partial delete: make null some of fields and remove some the images by query

            for partial delete>>

                after id/ set the query_params ?partial=true (?partial=<value that represent True in python>)
                add the fields you want to make null, put the value of them true

            Note: supported fields to make null: phone_number, description, txt_file, pdf_file, voice_file

                    ex) 127.0.0.1:8000/posts/1/?partial=true&phone_number=true&txt_file=true

                for delete the element of images(not make them null), put value of imgaes param to the ids of 
                the images you want to delete(seprate them by , ). to delete all images sent images=all

                    ex) 127.0.0.1:8000/posts/1/?partial=true&phone_number=true&imgages=1,2,3



        """
        partial = bool(request.query_params.get('partial', False))

        if not partial:
            return super().destroy(request, *args, **kwargs)

        self.get_serializer().partial_delete(instance=self.get_object(), params=request.query_params.dict())
        return super().retrieve(request, *args, **kwargs)




    def update(self, request, *args, **kwargs):
        """
                update:
                used to update fields(repalaces with new one)
                image, and name field is required to update(by put) and create
            Note: validation is like create method

        """
        partial = kwargs.get('partial', False)

        if not partial:
            self.get_serializer().delete_all_images(instance=self.get_object())
            return super().retrieve(request, *args, **kwargs)

        return super().update(request, *args, **kwargs)
    


    def partial_update(self, request, *args, **kwargs):
        """
                partial update:
                used to update partially fields
                images and name is not required
            Note: by patching the images, new images added(previuses exists), to replace all images with new images use put method\n
            Note: validation is like create method
        """
        return super().partial_update(request, *args, **kwargs)