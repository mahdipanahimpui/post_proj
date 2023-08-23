from django.shortcuts import render
from django.views import View
from django.shortcuts import HttpResponse
from rest_framework import viewsets
from . models import Post, PostImages
from . serializers import PostSerializer
from rest_framework.decorators import action




# class Home(View):
#     def get(self, request):
#         return HttpResponse('home page')



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['delete'])
    def delete_partial(self, request, pk=None, **kwargs):

        phone_number = bool(request.query_params.get('phone_number', False))
        description = bool(request.query_params.get('description', False))
        txt_file = bool(request.query_params.get('txt_file', False))
        pdf_file = bool(request.query_params.get('pdf_file', False))
        voice_file = bool(request.query_params.get('voice_file', False))
        images = request.query_params.get('images', False)
        images = images.split(',')
        images = [int(img) for img in images]

        print(images)
        return HttpResponse('hello')


    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)

        if not partial:
            self.get_serializer().delete_all_images(instance=self.get_object())

        return super().update(request, *args, **kwargs)