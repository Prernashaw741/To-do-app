from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

class loginView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if(email != None) and (password != None):
            try:
                db = User.objects.get(email = email, password = password)
                response = Response({
                    "status" : 200
                }, status=200)
                response.set_cookie(key="uid", value=db.pk)
                return response
            except User.DoesNotExist:
                return Response(status=404)
            
        else:
            return Response(data = {
                "status" : 400,
                "message" : "Invalid Credentials"
            }, status = 400)
        
class SignUpView(APIView):
    def post(self,request):
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if None in [name, email, password]:
            return Response(status=400)
        else:
            try:
                db = User.objects.create(name = name, email = email, password = password)
                return Response(status=200)
            except IntegrityError as e:
                return Response(data = {
                    "status" : "Already Exists "
                }, status = 400) 
            
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if(email != None) and (password != None):
            try:
                db = User.objects.get(email = email)
                db.password = password
                db.save()
                return Response(status = 200)
            except User.DoesNotExist:
                return Response(status = 400)