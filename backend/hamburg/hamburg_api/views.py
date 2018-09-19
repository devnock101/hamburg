from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from hamburg_api.models import WelcomeModel
from hamburg_api.serializer import WelcomeViewSerializer


class WelcomeView(generics.ListCreateAPIView):
    """Welcome/Test View"""
    queryset = WelcomeModel.objects.all()
    serializer_class = WelcomeViewSerializer
    http_method_names = ['get']
