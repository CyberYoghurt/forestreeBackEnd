from .models import Wood,Machinery,Product
from rest_framework import serializers
from django.contrib.auth.models import User

class UserWoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wood
        fields = ['id','name','image']


class UserMachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ['id','name','image']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','id']  


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class WoodListSerializer(serializers.ModelSerializer):
    owner = UserListSerializer(many=False,read_only=True)

    class Meta:
        model=Wood
        fields = '__all__'


class MachineryListSerializer(serializers.ModelSerializer):
    owner = UserListSerializer(many=False,read_only=True)

    class Meta:
        model=Machinery
        fields = '__all__'


class WoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wood
        fields = '__all__'

class MachinerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Machinery
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Product
        fields = '__all__'