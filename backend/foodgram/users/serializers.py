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
  """для страницы отдельного рецепта"""
  is_subscribed = serializers.SerializerMethodField()
  fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'password',
                  'is_subscribed'
                  ]
  
  
  # 1. вытащить из контекста id рецепта 
  # 2. подтянуть автора этого рецепта
  # 3. определить подписан ли уже юзер на автора 
  # 4. в зависимости от существования подписки вернуть значение 
  def get_is_subscribed(self, obj):
    pass
        # user = self.context.get('request').user
        # author = # recipe__author...
        # if Subscription.objects.filter(author=author,
        #                                user=user):
        #     return True
        # return False
            
