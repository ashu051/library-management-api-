from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book,Favourite

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
## if password is not hashing 
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['id','title','description','book_image']
class FavouriteSerializer(serializers.ModelSerializer):
    # kitab = serializers.StringRelatedField(many=True)
    # aadmi = serializers.StringRelatedField(many=True)
    # def _user(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return request.user
    # current_user = serializers.SerializerMethodField('_user')
    # print(current_user)

    # # Use this method for the custom field


    class Meta:
        model = Favourite
        fields=['id','book','user']
