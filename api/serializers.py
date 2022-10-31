from urllib import response
from rest_framework import serializers
from api.models import Todos
from django.contrib.auth.models import User

class TodoSerializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)

    # def create(self,request,*arg,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return response(data=serializer.data)
    #     else:
    #         return response(data=serializer.errors)
    class Meta:
        model=Todos
        fields=[
            "task_name",
            "user",
            "status"
            ]
    def create(self, validated_data):
        usr=self.context.get("user")
        return Todos.objects.create(**validated_data,user=usr)
            
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "email",
            "username",
            "password"
            ]
    def create(self,**validated_data):
        return User.objects.create_user(**validated_data)