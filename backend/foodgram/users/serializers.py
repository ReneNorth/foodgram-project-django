from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import logging

from subscription.models import Subscription

User = get_user_model()

logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)


class CustomUserSerializer(serializers.ModelSerializer):
    """Customized user serialiser. """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'password',
                  'is_subscribed'
                  ]
        lookup_field = 'username'
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        """Checks if the user is supscribed to the recipe's author"""
        log.info(f'user obj: {obj}')
        user_id = self.context.get('request').user.id
        if Subscription.objects.filter(user_id=user_id,
                                       author=obj).exists():
            return True
        return False

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    password=make_password(validated_data['password']))
        user.set_password(validated_data['password'])
        user.save()
        return user
