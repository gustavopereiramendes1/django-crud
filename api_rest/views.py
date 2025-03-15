from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializers
from .models import User


@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):
    
    try:
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializers(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        nickname = request.data['user_nickname']
        
        if nickname == user.pk:
            serializer = UserSerializers(user, data=request.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def user_manager(request):
    
    if request.method == 'GET':
        
        try:
            if request.GET['user']:
                
                user_nickname = request.GET['user']
                
                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserSerializers(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'POST':
        
        new_user = request.data
        serializer = UserSerializers(data=new_user)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'PUT':
        
        
        nickname = request.data['user_nickname']
        try:    
            updated_user = User.objects.get(pk=nickname)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializers(updated_user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        
        try:
        
            nickname = request.data['user_nickname']
            try:
                user_to_delete = User.objects.get(pk=nickname)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)    
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)