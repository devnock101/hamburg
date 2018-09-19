""" Serializer """

from rest_framework import serializers
from hamburg_api.models import WelcomeModel

class WelcomeViewSerializer(serializers.ModelSerializer):
    """ WelcomeViewSerializer"""
    class Meta:
        """ Meta """
        model = WelcomeModel
        fields = ('wId', 'wText')
