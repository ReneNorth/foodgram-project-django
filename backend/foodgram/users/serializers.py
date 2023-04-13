from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
from subscription.models import Subscription


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'password',
                #   'is_subscribed'
                  ]
        lookup_field = 'username'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    password=make_password(validated_data['password']))
        user.set_password(validated_data['password'])
        user.save()
        return user
      
class SubscribedUserSerializer(serializers.ModelSerializer):
  is_subscribed = serializers.SerializerMethodField()
  
  
  
  fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'password',
                  'is_subscribed'
                  ]
  def (self, obj):
        user_id = self.context.get("user_id")
        if user_id:
            return user_id in obj.my_objects.values_list("user_id", flat=True)
        return False
            
