from django.shortcuts import render,redirect

# Create your views here.
from .models import Category,Listing,User,Transaction
from .serializers import CategorySerializer,UserSerializer,TransactionSerializer,ListingSerializer,LoginSerializer,TransactionCreateSerializer
from rest_framework import generics,viewsets,permissions,status
from django.contrib.auth import login,logout,authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password



class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[permissions.AllowAny]
    
    def perform_create(self, serializer):
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
        # if user.is_staff:  # Check if the user is an admin
        #     return Listing.objects.all()
    
    
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



class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)


class LogoutApiView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')