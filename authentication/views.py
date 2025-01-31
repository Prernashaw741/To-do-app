from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...



class googleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token', None)
        if(token != None):
            try:
            
                # Specify the CLIENT_ID of the app that accesses the backend:
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), ["1001329610571-fr4j2raq6em0guc5etqmgglijnhaae1j.apps.googleusercontent.com"])

                # Or, if multiple clients access the backend server:
                # idinfo = id_token.verify_oauth2_token(token, requests.Request())
                # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
                #     raise ValueError('Could not verify audience.')

                # If the request specified a Google Workspace domain
                # if idinfo['hd'] != DOMAIN_NAME:
                #     raise ValueError('Wrong domain name.')

                # ID token is valid. Get the user's Google Account ID from the decoded token.
                userid = idinfo['sub']
                email = idinfo['email']
                print(idinfo["picture"])
                db = User.objects.get(email = email)
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