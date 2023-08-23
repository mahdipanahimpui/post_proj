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

    def destroy(self, request, *args, **kwargs):
        partial = bool(request.query_params.get('partial', False))

        if not partial:
            return super().destroy(request, *args, **kwargs)

        self.get_serializer().partial_delete(instance=self.get_object(), params=request.query_params.dict())
        return super().retrieve(request, *args, **kwargs)




    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)

        if not partial:
            self.get_serializer().delete_all_images(instance=self.get_object())

        return super().update(request, *args, **kwargs)