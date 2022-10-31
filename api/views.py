from urllib import request
from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todos
from api.serializers import TodoSerializer,RegistrationSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions



class TodosView(ViewSet):
    def list(self,request,*arg,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*arg,**kw):
        serializer=TodoSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*arg,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*arg,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*arg,**kw):
        id=kw.get("pk")
        obj=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TodosModelView(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)


    def create(self,request,*arg,**kw):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
        


    # def list(self,request,*arg,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*arg,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*arg,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=True)
    def mark_as_done(self,request,*arg,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=False
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)


class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self,request,*arg,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)