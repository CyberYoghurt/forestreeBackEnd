from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['isAdmin'] = user.is_superuser
        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    
    def get(self,request):
        print('reached change password')
        return Response(status=200)
    


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
  if(request.user.check_password(request.data['old'])==False):
    # oldpass is wrong
    return Response(status=401)

  if(request.data['pass1']!=request.data['pass2']):
    # new pass arent the same
    return Response(status=400)
       
  if(request.data['pass1'] == request.data['old']):
    # new password cant be the same as the old one'
    return Response(status=400)

  request.user.set_password(request.data['pass1'])
  request.user.save()
  return Response(status=200)

     
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_profile(request):
  try:
    print(request.data)
    if(request.data['username'] == ''):
      print('no username')
      return Response(status=400)
    
    request.user.email = request.data['email']
    request.user.username = request.data['username']
    request.user.first_name = request.data['firstName']
    request.user.last_name = request.data['lastName']
    request.user.save()



    return Response(status=200)

  except Exception as e:
    print(e)
    return Response(status=400)
     
   
     


        

@api_view(['GET'])
def getRoutes(request):
  routes = [
    'api/token',
    'api/token/refresh',
  ]
  return Response(routes)


