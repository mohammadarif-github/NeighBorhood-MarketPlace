from rest_framework import serializers
from .models import User,Category,Listing,Transaction

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
        
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)