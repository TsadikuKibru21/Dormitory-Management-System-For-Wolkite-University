from rest_framework import serializers
from .models import Messages

from account.models import UserAccount
class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserAccount.objects.all())
    receiver_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserAccount.objects.all())

    class Meta:
        model = Messages
        fields = ['sender_name', 'receiver_name', 'description', 'time']

