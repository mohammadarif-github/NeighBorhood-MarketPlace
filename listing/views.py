from django.shortcuts import render,redirect

# Create your views here.
from .models import Category,Listing,User,Transaction
from .serializers import CategorySerializer,UserSerializer,TransactionSerializer,ListingSerializer,TransactionCreateSerializer,CustomTokenObtainPairSerializer
from rest_framework import generics,viewsets,permissions,status
from django.contrib.auth import login,logout,authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken




from rest_framework.exceptions import ValidationError

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        username = self.request.data.get('username')
        email = self.request.data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': ['This username is already taken.']})
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': ['This email is already registered.']})

        raw_password = self.request.data.get('password')
        encrypted_pass = make_password(raw_password)
        serializer.save(password=encrypted_pass)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        if self.request.user == self.get_object():
            serializer.save()
        else :
            raise PermissionDenied("You do not have permission to perform this action.")


class ListingView(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        if self.request.user == self.get_object().user:
            serializer.save()
        else :
            raise PermissionDenied("You do not have permission to perform this action.")
    
    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to perform this action.")

class UserListingView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        user = self.request.user
        return Listing.objects.filter(user=user)
    
    
class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TransactionCreateSerializer
        return TransactionSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(buyer=user)
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
        
    def perform_update(self, serializer):
        if self.request.user == self.get_object().buyer:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to perform this action.")
    
    def perform_destroy(self, instance):
        if self.request.user == instance.buyer:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class LoginApiView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
                
            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
