from django.urls import path
from rest_framework import routers
from . import views


app_name = 'home'

urlpatterns = [

]
    

router = routers.SimpleRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns += router.urls




