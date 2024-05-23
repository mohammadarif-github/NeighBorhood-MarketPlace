from rest_framework import serializers
from .models import User,Category,Listing,Transaction

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email",'username','first_name','last_name','phone','address','image']
        
class ListingSerializer(serializers.ModelSerializer):
    class Meta :
        model = Listing
        fields = "__all__"
        
class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['listing', 'status']
        

class TransactionSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()
    buyer = UserSerializer()
    date = serializers.DateTimeField(format="%d-%m-%y %H:%M:%S")

    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'date', 'status', 'listing']
          
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta : 
        model = Category
        fields = "__all__"
        
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Include additional responses here
        data.update({'user_id': self.user.id})

        return data
    
    
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)