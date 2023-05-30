from rest_framework import serializers

from .models import *


class ProjectBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBasicInfo
        fields = '__all__'

class ProjectTokenInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTokenInfo
        fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name', 'image', 'basic_info','token_info')
        depth = 1
